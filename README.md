# 🤖 LinkedIn Setter — Template

Un chatbot d'**appointment setting** sur LinkedIn : il répond à tes DM, qualifie tes prospects et **booke des appels** à ta place, dans ta voix, adapté à ton business. Tu n'as pas besoin d'être développeur — ton **Claude Code** fait l'installation, tu remplis juste tes infos et tes clés.

> Ce dépôt est un **template**. Tu le dupliques sur TON compte, tu le remplis avec TON business, et tu le déploies. Aucune info du créateur n'y figure : tout est à toi.

---

## 🧩 Comment ça marche (2 briques)

```
┌──────────────── n8n (la tuyauterie, sur ton compte) ───────────────┐
│ DM LinkedIn reçu → scrape profil → historique → analyse → 📡 brain  │
│ → renvoie la réponse en DM → te notifie sur Telegram                │
└─────────────────────────────────────────────────────────────────────┘
                              ↕
┌──────────── ce dépôt = le "brain" (déployé sur Railway) ────────────┐
│ FastAPI + Claude. Charge TA persona + TES principes + TES skills.    │
│ Reçoit la conversation, renvoie LE message à envoyer.                │
└──────────────────────────────────────────────────────────────────────┘
```

- **Le brain (ce dépôt)** = l'intelligence du bot. C'est ici que tu mets ton offre, tes objections, ton ton.
- **n8n** = la plomberie qui relie LinkedIn au brain (fourni séparément, à importer).

---

## ✅ Ce que TU dois faire toi-même (Claude Code ne peut pas)

1. **Créer tes comptes / clés API** (voir [INSTALL.md](INSTALL.md) pour le détail clic-par-clic) :
   - **Anthropic** (le cœur — fait tourner le bot) → console.anthropic.com + crédits
   - **OpenAI** (analyse + transcription des vocaux, côté n8n)
   - **Unipile** (accès LinkedIn)
   - **Apify** (scraping de profil)
   - **Telegram** (notifications)
   - Comptes : **GitHub**, **Railway**, **n8n Cloud**
2. **Remplir les fichiers marqués `🟨 À REMPLIR`** avec ton business (ton offre, tes objections, ta bio…).

## 🤖 Ce que ton Claude Code fait pour toi

- Dupliquer ce template dans ton projet et t'aider à remplir les fichiers (il t'interviewe, rédige, tu valides)
- Créer ton `.env`
- Déployer le brain sur Railway
- Importer et câbler le workflow n8n
- Vérifier que tout tourne

---

## 🚀 Démarrage : le prompt à donner à ton Claude Code

Ouvre Claude Code dans un dossier vide, et colle le contenu de **[claude-code/1-install.md](claude-code/1-install.md)**. Il te guide pour tout le reste.

Avant ça, lis **[INSTALL.md](INSTALL.md)** pour créer tes clés API (tu en auras besoin pendant l'install).

---

## 📁 Structure

```
├── main.py / config.py        ← le moteur (n'y touche pas, c'est générique)
├── .env.example               ← copie en .env et remplis tes clés
├── prompts/
│   ├── personas/me.md         🟨 ton identité
│   ├── principes.md           🟨 ton offre (le reste = méthodo générique)
│   └── skills/
│       ├── business-info.md   🟨 ton offre détaillée
│       ├── objections.md      🟨 tes objections + tes cassages
│       ├── bio-detail.md      🟨 ton parcours
│       ├── phase-1..5.md      ← méthodo de setting (générique, quelques 🟨 à adapter)
│       └── [10 livres].md     ← frameworks de persuasion (génériques, ne pas toucher)
├── claude-code/               ← les prompts à coller dans ton Claude Code
└── n8n/                       ← le workflow à importer dans n8n
```
