# 🚀 Installer ton chatbot LinkedIn — Guide

> Principe : tu crées tes comptes + tes clés, puis tu ouvres **Claude Code dans un dossier vide** et tu
> lui colles **une seule phrase**. À partir de là, Claude Code installe **tout** (template, déploiement,
> branchement LinkedIn) en te demandant tes clés au fur et à mesure.

---

## ✅ ÉTAPE 1 — Crée tes comptes et tes clés (la seule partie 100% manuelle)

Ouvre l'app **Notes**. Pour chaque service : crée un compte, et copie la clé dans tes notes.

### Les clés du bot
1. **Anthropic** (le cerveau) — `https://platform.claude.com/settings/billing` → mets 20-50 € de crédits → **API Keys** → **Create Key** → copie `sk-ant-...`
2. **OpenAI** — `platform.openai.com` → **Billing** (carte + crédits) → **API keys** → **Create new secret key** → copie `sk-...`
3. **Unipile** — `unipile.com` → **Dashboard** → **connecte ton compte LinkedIn** (suis leur assistant) → copie ta **API Key** + ton **DSN**
4. **Apify** — `apify.com` → **Settings → Integrations → API tokens** → copie le **token**
5. **Telegram** — dans l'app, écris à **@BotFather** → `/newbot` → copie le **token** du bot

### Les accès pour que Claude Code automatise le reste
6. **GitHub** — `github.com` → ta photo → **Settings → Developer settings → Personal access tokens → Tokens (classic)** → **Generate** → coche **`repo`** → copie le token `ghp_...`
7. **Railway** — `railway.com` (crée le compte) → ta photo → **Account Settings → Tokens** → **New Token** → copie-le
8. **n8n** — `n8n.io` → crée un espace **n8n Cloud** → **Settings → n8n API** → **Create API key** → copie-la

> 💳 À savoir honnêtement : Anthropic/OpenAI/Apify se paient à l'usage, et Railway + n8n Cloud sont
> payants (quelques €/mois). Prévois une carte bancaire.

---

## ✅ ÉTAPE 2 — Ouvre Claude Code dans un dossier VIDE

1. Crée un nouveau dossier vide sur ton ordi (ex : `mon-bot`).
2. Ouvre **VS Code** → menu **File → Open Folder** → choisis ce dossier `mon-bot` → **Open**.
3. Ouvre **Claude Code** (l'extension dans VS Code). Il est maintenant prêt, dans ton dossier vide.

*(Pas encore Claude Code ? Installe l'extension Claude Code dans VS Code, ou l'app officielle d'Anthropic.)*

---

## ✅ ÉTAPE 3 — Colle CETTE phrase à Claude Code

Copie-colle exactement ça dans Claude Code, et appuie sur Entrée :

> **Clone le dépôt https://github.com/louvideosia-png/linkedin-setter-template.git dans le dossier courant, puis lis le fichier `claude-code/INSTALLER.md` et suis-le entièrement pour installer mon chatbot LinkedIn. Demande-moi mes clés au fur et à mesure.**

C'est tout. À partir d'ici, Claude Code va :
- récupérer le template,
- **t'interviewer sur ton business** et remplir le bot pour toi (tu valides),
- te **demander tes clés une par une** (tu les colles quand il les demande),
- **déployer** le bot sur Railway, **brancher** n8n et **relier** ton LinkedIn,
- et te faire **tester**.

Réponds simplement à ses questions. Quand il te demande de faire un clic qu'il ne peut pas faire
(ex : autoriser une connexion), il te dira exactement où cliquer.

---

## ✅ ÉTAPE 4 — Le test final

Quand Claude Code te le demande : depuis un **autre** compte LinkedIn, envoie-toi un message privé.
Le bot doit répondre tout seul. 🎉
*(Astuce : au début, Claude Code met ton compte de test en "allowlist" pour que le bot ne réponde
qu'à toi le temps de vérifier ; ensuite il passe en mode production.)*

---

## 🆘 Si ça bloque
Dis simplement à Claude Code ce qui se passe (copie-lui le message d'erreur), il corrige avec toi.
Causes les plus fréquentes : **crédits Anthropic vides**, une **clé oubliée**, ou un compte (Railway/n8n)
pas encore créé.
