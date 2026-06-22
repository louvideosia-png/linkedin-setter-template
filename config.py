"""Configuration centrale — TOUT ce qui est propre à ton business vient d'ici.

Les valeurs sont lues depuis les variables d'environnement (fichier .env en local,
ou variables Railway en production). Aucune info personnelle n'est codée en dur ici :
tu remplis ton .env (voir .env.example), et c'est tout.
"""

import os

# --- Identité du persona (toi) ---
# PERSONA_KEY doit correspondre au nom du fichier dans prompts/personas/ (sans .md).
# Par défaut "me" → prompts/personas/me.md
PERSONA_KEY = os.getenv("PERSONA_KEY", "me")
# Le prénom affiché dans l'historique de conversation envoyé au modèle.
PERSONA_DISPLAY_NAME = os.getenv("PERSONA_DISPLAY_NAME", "Moi")

# --- Liens canoniques de ton offre ---
# Le bot ne les écrit JAMAIS à la main : il appelle un tool qui renvoie ces URLs.
# Laisse vide ("") un lien que tu n'utilises pas — le tool correspondant le signalera.
CALENDLY_URL = os.getenv("CALENDLY_URL", "")
YOUTUBE_URL = os.getenv("YOUTUBE_URL", "")
WEBSITE_URL = os.getenv("WEBSITE_URL", "")

# --- Modèle & limites (réglages avancés, valeurs par défaut OK) ---
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
MAX_THINKING_TOKENS = int(os.getenv("MAX_THINKING_TOKENS", "8000"))
MAX_TURNS = int(os.getenv("MAX_TURNS", "15"))

# Signal interne de handover (ne pas changer)
HANDOVER_SIGNAL = "PAUSE_CONVERSATION"
