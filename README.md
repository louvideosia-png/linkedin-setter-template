# 🤖 LinkedIn Setter — Template

Un chatbot d'**appointment setting** sur LinkedIn : il répond à tes DM, qualifie tes prospects et **booke des appels** à ta place, dans ta voix, adapté à ton business. Tu n'as pas besoin d'être développeur — ton **Claude Code** fait l'installation, tu remplis juste tes infos et tes clés.

> Ce dépôt est un **template**. Tu le dupliques sur TON compte, tu le remplis avec TON business, et tu le déploies.

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

- **Le brain (ce dépôt)** = l'intelligence du bot. C'est ici que tu mets ton offre, tes objections, etc.
- **n8n** = la plomberie qui relie LinkedIn au brain (fourni séparément, à importer).

---

## 🚀 Pour l'installer

👉 **Suis le guide unique : [COMMENCER-ICI.md](COMMENCER-ICI.md)** — tout est expliqué pas à pas (créer tes clés, récupérer le template, lancer Claude Code, tester).

En résumé : tu crées tes clés API + tu remplis tes infos business, et ton **Claude Code** fait tout le reste (remplissage, déploiement Railway, câblage n8n).

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
