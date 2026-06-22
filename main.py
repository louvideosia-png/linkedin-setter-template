import asyncio
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import config

load_dotenv()

# Valeurs propres au business — viennent de config.py (lui-même alimenté par le .env)
CANONICAL_CALENDLY = config.CALENDLY_URL
CANONICAL_YOUTUBE = config.YOUTUBE_URL
CANONICAL_WEBSITE = config.WEBSITE_URL
HANDOVER_SIGNAL = config.HANDOVER_SIGNAL

MODEL = config.MODEL
MAX_THINKING_TOKENS = config.MAX_THINKING_TOKENS
MAX_TURNS = config.MAX_TURNS

PROMPTS_DIR = Path(__file__).parent / "prompts"
PERSONAS_DIR = PROMPTS_DIR / "personas"
SKILLS_DIR = PROMPTS_DIR / "skills"

PERSONA_CACHE: dict[str, str] = {
    p.stem: p.read_text(encoding="utf-8") for p in PERSONAS_DIR.glob("*.md")
}
PRINCIPES = (PROMPTS_DIR / "principes.md").read_text(encoding="utf-8")

# Skills loaded on demand by the bot via load_skill(name) tool.
SKILLS_CACHE: dict[str, str] = {
    s.stem: s.read_text(encoding="utf-8") for s in SKILLS_DIR.glob("*.md")
}

DEFAULT_PERSONA = config.PERSONA_KEY


def build_full_system_prompt(persona: str) -> str:
    """System prompt = persona injecté en haut, puis le doc 'principes premiers'."""
    persona_block = PERSONA_CACHE.get(persona) or next(iter(PERSONA_CACHE.values()), "")
    return f"{persona_block}\n\n---\n\n{PRINCIPES}"


SYSTEM_PROMPTS: dict[str, str] = {
    p: build_full_system_prompt(p) for p in PERSONA_CACHE.keys()
}


@tool(
    "get_calendly_link",
    "Retourne l'URL canonique de ton Calendly. UTILISE ce tool dès que tu veux partager le lien de réservation — ne jamais écrire l'URL à la main.",
    {},
)
async def get_calendly_link(args):
    url = CANONICAL_CALENDLY or "(aucun lien Calendly configuré — ne propose pas de réservation par lien)"
    return {"content": [{"type": "text", "text": url}]}


@tool(
    "get_youtube_link",
    "Retourne l'URL canonique de ta vidéo / mini-VSL. UTILISE ce tool dès que tu veux partager la vidéo.",
    {},
)
async def get_youtube_link(args):
    url = CANONICAL_YOUTUBE or "(aucune vidéo configurée — ne propose pas de vidéo)"
    return {"content": [{"type": "text", "text": url}]}


@tool(
    "get_website_link",
    "Retourne l'URL canonique de ton site qui détaille l'offre, le mécanisme, les tarifs et la garantie. UTILISE ce tool quand le prospect demande plus d'infos sur l'offre, le fonctionnement, les tarifs, ou veut creuser avant de réserver. Tu envoies une brève explication de ta voix + le lien pour creuser.",
    {},
)
async def get_website_link(args):
    url = CANONICAL_WEBSITE or "(aucun site configuré — explique de vive voix sans lien)"
    return {"content": [{"type": "text", "text": url}]}


@tool(
    "load_skill",
    (
        "Charge le contenu d'une skill à la demande. Les skills sont des fiches que tu peux invoquer "
        "quand ton instinct le justifie — pas par défaut. Si tu doutes qu'une skill t'aide → ne charge pas.\n\n"
        ""
        "PHASES DU FIL ROUGE (charge la skill de la phase courante quand tu veux le détail tactique) :\n"
        "- `phase-1-defiance` — chitchat, casser la méfiance, signaux d'ouverture\n"
        "- `phase-2-acquisition` — faire émerger le pain + mini-transformation + offre modulaire\n"
        "- `phase-3-asset` — asset de valeur matché au pain + réciprocité\n"
        "- `phase-4-call` — proposer le call en 2 temps (4a tester l'intention, 4b envoyer le lien)\n"
        "- `phase-5-post-booking` — protéger le call, less is more, aucun ask\n\n"
        ""
        "TES FICHES BUSINESS (à remplir, propres à ton activité) :\n"
        "- `objections` — bibliothèque de cassages d'objections et fausses croyances. "
        "À charger DÈS QUE le prospect formule une objection ou une croyance qui s'oppose à ton offre.\n"
        "- `bio-detail` — ton parcours complet et tes preuves sociales. "
        "À charger quand le prospect demande qui tu es, ton parcours, ta crédibilité.\n"
        "- `business-info` — ton offre détaillée, ton mécanisme, et les réponses canoniques "
        "aux questions pièges sur ton offre.\n\n"
        ""
        "10 LIVRES DE PERSUASION (références génériques) :\n"
        "cialdini-influence, cialdini-presuasion, voss-never-split, carnegie-win-friends, "
        "greene-human-nature, pink-to-sell-is-human, dixon-challenger-sale, fitzpatrick-mom-test, "
        "rackham-spin-selling, kahneman-thinking.\n\n"
        ""
        "ARGS :\n"
        "- name : le nom exact de la skill (kebab-case sans extension)"
    ),
    {"name": str},
)
async def load_skill(args):
    name = (args.get("name") or "").strip()
    content = SKILLS_CACHE.get(name)
    if not content:
        available = ", ".join(sorted(SKILLS_CACHE.keys()))
        return {"content": [{"type": "text", "text": f"Skill '{name}' introuvable. Disponibles : {available}"}], "is_error": True}
    return {"content": [{"type": "text", "text": content}]}


@tool(
    "request_handover",
    "Demande un handover humain (tu prends le relais). UTILISE UNIQUEMENT si : (1) le prospect demande explicitement à parler à un humain, (2) frustration ou colère significative, (3) sujet sensible (santé, deuil, crise perso), (4) tu n'as pas l'info nécessaire pour répondre correctement, (5) incohérence repérée que tu ne peux pas résoudre. Reason = en quelques mots, pourquoi.",
    {"reason": str},
)
async def request_handover(args):
    return {"content": [{"type": "text", "text": f"HANDOVER_REQUESTED::{args.get('reason', 'unspecified')}"}]}


SETTER_MCP_SERVER = create_sdk_mcp_server(
    name="setter_tools",
    version="1.0.0",
    tools=[
        get_calendly_link,
        get_youtube_link,
        get_website_link,
        load_skill,
        request_handover,
    ],
)

ALLOWED_TOOLS = [
    "mcp__setter_tools__get_calendly_link",
    "mcp__setter_tools__get_youtube_link",
    "mcp__setter_tools__get_website_link",
    "mcp__setter_tools__load_skill",
    "mcp__setter_tools__request_handover",
]


app = FastAPI(title="Setter Agent")


class HistoryMessage(BaseModel):
    role: Literal["prospect", "me"]
    text: str


class ChatRequest(BaseModel):
    history: list[HistoryMessage] = Field(default_factory=list)
    last_message: str
    lead_profile: str = ""
    agent_persona: str = DEFAULT_PERSONA
    chat_id: str = ""
    sender_account_id: str = ""


class ChatResponse(BaseModel):
    messages: list[str]
    handover: bool
    handover_reason: str = ""
    raw: str
    tools_called: list[str] = Field(default_factory=list)
    cost_usd: float | None = None
    duration_ms: int | None = None
    num_turns: int | None = None


def build_user_prompt(req: ChatRequest) -> str:
    persona_label = config.PERSONA_DISPLAY_NAME
    transcript_lines = []
    for m in req.history:
        speaker = persona_label if m.role == "me" else "Prospect"
        transcript_lines.append(f"{speaker}: {m.text}")
    transcript = (
        "\n".join(transcript_lines) if transcript_lines else "(conversation vide, premier échange)"
    )
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"""Date du jour : {today} (utilise cette année et pas une autre quand tu mentionnes une date).

Profil du prospect (ce que tu SAIS DÉJÀ — c'est SA bio publique scrapée + analyse). Règles d'usage :
  ❌ Tu ne lui demandes JAMAIS une info qui est déjà ici (= signal d'incompétence = perte de crédibilité immédiate)
  ❌ Tu ne lui demandes JAMAIS son ICP cible en question ouverte multi-choix
  ✅ Tu DÉDUIS son ICP / sa cible / son contexte business à partir de son Occupation + Topics + Personalization
  ✅ Si tu hésites sur ta déduction, tu la proposes comme HYPOTHÈSE à valider en 1 phrase. JAMAIS comme question ouverte.
{req.lead_profile or "(pas de profil disponible)"}

Historique de la conversation (chronologique) :
{transcript}

Dernier message reçu du prospect :
{req.last_message}

═══════════════════════════════════════════════════════════════════
PRODUIS MAINTENANT le ou les messages que tu vas envoyer au prospect.
═══════════════════════════════════════════════════════════════════

⚠️ FORMAT DE SORTIE ABSOLU :
Ta sortie texte = EXACTEMENT ce que le prospect va recevoir mot pour mot dans son DM LinkedIn.
RIEN d'autre. C'est-à-dire :

❌ ZÉRO préambule, zéro analyse écrite, zéro diagnostic verbalisé
❌ ZÉRO explication de ton raisonnement
❌ ZÉRO méta-commentaire sur ta stratégie
❌ ZÉRO description de ton processus mental

✅ UNIQUEMENT les messages exacts à envoyer, séparés par `<<NEXT>>` si plusieurs bulles.

Tout ton diagnostic, ta lecture du prospect, ta mobilisation des principes — TOUT ça se fait en pensée (extended thinking interne), JAMAIS en texte visible au prospect. Si tu écris "Je vais analyser…" en tête de ta sortie, c'est un BUG GRAVE : le prospect le lit, sait que c'est une IA, et tu perds le call.

Tes messages sortent comme si tu tapais vite sur LinkedIn — chaleureux, casual, pas un robot qui pense à haute voix."""


RATE_LIMIT_PATTERNS = [
    "429",
    "rate limit",
    "rate_limit",
    "exceed your organization",
    "exceed your account",
    "input tokens per minute",
    "output tokens per minute",
    "requests per minute",
]
OTHER_API_ERROR_PATTERNS = [
    "api error",
    "request rejected",
    "internal server error",
    "server error",
    "connection error",
    "authentication_error",
    "permission_error",
    "claude.com/en/api",
    "console.anthropic.com",
    "credit balance is too low",
    "credit balance",
    "insufficient credit",
    "insufficient funds",
    "insufficient_funds",
    "out of credits",
    "billing_error",
    "billing error",
    "your account has been suspended",
    "account suspended",
    "402",
    "payment required",
    "anthropic-version",
    "invalid_request_error",
    "overloaded_error",
    "api_error",
]


def looks_like_suspicious_short_error(text: str) -> bool:
    if not text:
        return False
    if len(text) > 150:
        return False
    lowered = text.lower()
    suspicious_words = [
        "credit", "balance", "error", "failed", "exception",
        "timeout", "unavailable", "exceeded", "limit reached",
        "try again later", "503", "504", "500",
    ]
    return any(w in lowered for w in suspicious_words)
RETRY_BACKOFF_SECONDS = [5, 15, 30]


def looks_like_rate_limit(text: str) -> bool:
    lowered = (text or "").lower()
    return any(pat in lowered for pat in RATE_LIMIT_PATTERNS)


def looks_like_api_error(text: str) -> bool:
    lowered = (text or "").lower()
    return any(pat in lowered for pat in RATE_LIMIT_PATTERNS + OTHER_API_ERROR_PATTERNS)


META_LEAK_PATTERNS = [
    "je vais d'abord analyser",
    "je vais analyser",
    "d'abord, j'analyse",
    "d'abord j'analyse",
    "je commence par analyser",
    "analysons la situation",
    "analyse de la situation",
    "le prospect est ",
    "le prospect semble",
    "le prospect montre",
    "c'est un moment de",
    "pas besoin de lookup",
    "pas besoin d'appeler",
    "lookup tools ici",
    "lookup_tool",
    "mon raisonnement",
    "mon analyse interne",
    "voici mon analyse",
    "voici ma réponse",
    "je dois maintenant",
    "je vais maintenant",
    "ma stratégie ici",
    "stratégiquement, je",
    "pour bien faire, je",
    "première étape",
    "deuxième étape",
    "étape 1 :",
    "étape 2 :",
    "mobilise les leviers",
    "mobiliser les principes",
    "diagnostique",
    "diagnostic :",
    "internal :",
    "[analyse]",
    "[diagnostic]",
    "[réflexion]",
]


def looks_like_meta_leak(text: str) -> bool:
    if not text:
        return False
    head = text[:400].lower()
    return any(pat in head for pat in META_LEAK_PATTERNS)


def sanitize_human_style(text: str) -> str:
    """Strip AI tells (typographic punctuation, smart quotes) before sending to prospect."""
    if not text:
        return text
    replacements = {
        "—": ", ",
        "–": "-",
        "…": "...",
        "«": '"',
        "»": '"',
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        " ": " ",
        " ": " ",
    }
    out = text
    for k, v in replacements.items():
        out = out.replace(k, v)
    while "  " in out:
        out = out.replace("  ", " ")
    out = out.replace(" :", ":").replace(" ;", ";")
    out = out.replace(" ,", ",").replace(",,", ",")
    return out.strip()


def parse_final_text(text: str) -> tuple[list[str], bool, str]:
    text = text.strip()
    if not text:
        return [], True, "empty_response_from_agent"
    if text == HANDOVER_SIGNAL or "HANDOVER_REQUESTED::" in text:
        return [], True, ""
    if looks_like_api_error(text):
        return [], True, f"api_error_detected: {text[:300]}"
    if looks_like_suspicious_short_error(text):
        return [], True, f"suspicious_short_error_response: {text[:300]}"
    if looks_like_meta_leak(text):
        return [], True, f"meta_reasoning_leak_detected: {text[:300]}"
    parts = [p.strip() for p in text.split("<<NEXT>>") if p.strip()]
    if not parts:
        return [], True, "no_parsable_message"
    parts = [sanitize_human_style(p) for p in parts]
    parts = [p for p in parts if p]
    if not parts:
        return [], True, "no_parsable_message_after_sanitize"
    if any(looks_like_meta_leak(p) for p in parts):
        return [], True, "meta_reasoning_leak_detected_post_sanitize"
    if any(looks_like_suspicious_short_error(p) for p in parts):
        return [], True, "suspicious_short_error_post_sanitize"
    return parts, False, ""


@app.get("/")
async def root():
    return {
        "status": "alive",
        "model": MODEL,
        "personas_available": list(PERSONA_CACHE.keys()),
        "default_persona": DEFAULT_PERSONA,
        "system_prompt_chars_by_persona": {p: len(s) for p, s in SYSTEM_PROMPTS.items()},
        "principes_chars": len(PRINCIPES),
        "tools": [t.split("__")[-1] for t in ALLOWED_TOOLS],
        "max_thinking_tokens": MAX_THINKING_TOKENS,
        "max_turns": MAX_TURNS,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY non configurée")

    persona = req.agent_persona if req.agent_persona in SYSTEM_PROMPTS else DEFAULT_PERSONA
    if persona not in SYSTEM_PROMPTS and SYSTEM_PROMPTS:
        persona = next(iter(SYSTEM_PROMPTS))
    system_prompt = SYSTEM_PROMPTS[persona]

    user_prompt = build_user_prompt(req)

    options = ClaudeAgentOptions(
        model=MODEL,
        system_prompt=system_prompt,
        mcp_servers={"setter_tools": SETTER_MCP_SERVER},
        allowed_tools=ALLOWED_TOOLS,
        max_turns=MAX_TURNS,
        max_thinking_tokens=MAX_THINKING_TOKENS,
        permission_mode="bypassPermissions",
    )

    raw = ""
    tools_called: list[str] = []
    handover = False
    handover_reason = ""
    cost_usd: float | None = None
    duration_ms: int | None = None
    num_turns: int | None = None
    attempts_used = 0
    last_error_summary = ""

    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        attempts_used = attempt + 1
        raw_chunks_local: list[str] = []
        tools_called_local: list[str] = []
        handover_local = False
        handover_reason_local = ""
        try:
            async with ClaudeSDKClient(options=options) as client:
                await client.query(user_prompt)
                async for msg in client.receive_response():
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                raw_chunks_local.append(block.text)
                            elif isinstance(block, ToolUseBlock):
                                tool_short = block.name.split("__")[-1]
                                tools_called_local.append(tool_short)
                                if tool_short == "request_handover":
                                    handover_local = True
                                    handover_reason_local = (block.input or {}).get("reason", "")
                    elif isinstance(msg, ResultMessage):
                        cost_usd = getattr(msg, "total_cost_usd", None)
                        duration_ms = getattr(msg, "duration_ms", None)
                        num_turns = getattr(msg, "num_turns", None)
            raw_local = "\n".join(raw_chunks_local).strip()
            if looks_like_rate_limit(raw_local) and attempt < len(RETRY_BACKOFF_SECONDS):
                wait = RETRY_BACKOFF_SECONDS[attempt]
                last_error_summary = f"rate_limit_in_response (attempt {attempt+1}, waiting {wait}s)"
                await asyncio.sleep(wait)
                continue
            raw = raw_local
            tools_called = tools_called_local
            handover = handover_local
            handover_reason = handover_reason_local
            break
        except Exception as e:
            err_summary = f"{type(e).__name__}: {str(e)[:300]}"
            last_error_summary = err_summary
            is_rate_limit = looks_like_rate_limit(err_summary) or looks_like_rate_limit(str(e))
            if is_rate_limit and attempt < len(RETRY_BACKOFF_SECONDS):
                wait = RETRY_BACKOFF_SECONDS[attempt]
                await asyncio.sleep(wait)
                continue
            return ChatResponse(
                messages=[],
                handover=True,
                handover_reason=f"agent_loop_exception (attempt {attempt+1}): {err_summary}",
                raw="",
                tools_called=tools_called_local,
                cost_usd=cost_usd,
                duration_ms=duration_ms,
                num_turns=num_turns,
            )
    else:
        return ChatResponse(
            messages=[],
            handover=True,
            handover_reason=f"max_retries_exceeded ({attempts_used} attempts): {last_error_summary}",
            raw="",
            tools_called=tools_called,
            cost_usd=cost_usd,
            duration_ms=duration_ms,
            num_turns=num_turns,
        )

    messages, handover_from_text, handover_reason_from_text = parse_final_text(raw)
    handover = handover or handover_from_text
    if handover_reason_from_text and not handover_reason:
        handover_reason = handover_reason_from_text

    return ChatResponse(
        messages=messages,
        handover=handover,
        handover_reason=handover_reason,
        raw=raw,
        tools_called=tools_called,
        cost_usd=cost_usd,
        duration_ms=duration_ms,
        num_turns=num_turns,
    )
