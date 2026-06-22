# 📋 Guide d'installation complet — LinkedIn Setter

Ce guide te permet d'installer, **sans être développeur**, un chatbot qui répond à tes DM LinkedIn,
qualifie tes prospects et **booke des appels** à ta place, dans ta voix et adapté à ton business.

> Tu n'écris **aucune ligne de code**. Tu fais 2 choses : (1) créer tes comptes/clés API, et
> (2) remplir tes infos business. **Ton Claude Code fait tout le reste** (installation, déploiement,
> câblage) grâce à 3 prompts prêts à copier-coller.

---

## 🧠 Comment ça marche (à lire une fois)

Le bot a **2 briques** :

```
┌──────────── n8n (la "tuyauterie", sur ton compte n8n Cloud) ────────────┐
│ Un DM LinkedIn arrive → on récupère le profil + l'historique → on analyse │
│ → 📡 on appelle ton "brain" → on renvoie la réponse en DM → notif Telegram │
└───────────────────────────────────────────────────────────────────────────┘
                                  ↕
┌──────────── le "brain" (ce dépôt, déployé sur Railway) ──────────────────┐
│ L'intelligence : ta persona, ton offre, tes objections, ta voix.          │
│ Reçoit la conversation, renvoie LE message à envoyer.                      │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Le brain** = ce que tu remplis avec TON business.
- **n8n** = la plomberie (un workflow tout prêt à importer).

---

## ⏱️ Avant de commencer

- **Temps** : ~1h à 1h30 la première fois.
- **Pré-requis** : un ordinateur avec **Claude Code** installé, et une **carte bancaire**.
- **Coût mensuel indicatif** : crédits Anthropic + OpenAI (à l'usage), Apify, Unipile, et l'hébergement
  Railway + n8n Cloud. Compte quelques dizaines d'€/mois selon ton volume de conversations.

---

## 🔑 ÉTAPE 1 — Créer tes clés API (toi, manuel)

Garde un bloc-notes ouvert et colle chaque clé au fur et à mesure. **Ne partage ces clés avec personne.**

| Service | À quoi ça sert | Où | Ce que tu récupères |
|---|---|---|---|
| **Anthropic** ⭐ | fait tourner le bot (le cœur) | console.anthropic.com | une clé `sk-ant-...` **+ des crédits** |
| **OpenAI** | analyse + transcription des vocaux | platform.openai.com | une clé `sk-...` **+ des crédits** |
| **Unipile** | accès à ta messagerie LinkedIn | unipile.com | **API key**, **DSN**, **Account ID**, **Provider ID** |
| **Apify** | récupère le profil du prospect | apify.com | un **API token** |
| **Telegram** | te notifie les leads chauds | @BotFather dans Telegram | un **token de bot** |

Et crée 3 comptes : **GitHub** (github.com), **Railway** (railway.com), **n8n Cloud** (n8n.io).

> Détail de chaque clé clic-par-clic : voir la section **Annexe — créer les clés** en bas de ce guide.

---

## 🤖 ÉTAPE 2 — Dupliquer le template (ton Claude Code)

1. Sur **GitHub**, ouvre ce dépôt template → bouton **Use this template** → **Create a new repository**
   → nomme-le (ex `mon-setter`) → **Private** → Create.
2. Clone-le sur ton ordi (ou télécharge le ZIP et dézippe-le).
3. Ouvre **Claude Code** dans ce dossier.
4. Copie-colle le prompt **[claude-code/1-install.md](claude-code/1-install.md)**.

➡️ Ton Claude Code t'interviewe sur ton business, **remplit pour toi** tous les fichiers `🟨`
(ta persona, ton offre, tes objections, ta bio…), crée ton `.env`, teste le brain en local, et
pousse sur ton GitHub.

**Les fichiers que tu personnalises** (ton CC t'aide à chaque fois) :
- `prompts/personas/me.md` — qui tu es
- `prompts/principes.md` — ce que tu vends (zones 🟨 uniquement)
- `prompts/skills/business-info.md` — ton offre en détail
- `prompts/skills/objections.md` — les objections que tu entends + tes réponses
- `prompts/skills/bio-detail.md` — ton parcours et tes preuves

---

## 🤖 ÉTAPE 3 — Déployer le brain sur Railway (ton Claude Code)

Colle le prompt **[claude-code/2-deploy-railway.md](claude-code/2-deploy-railway.md)**.

➡️ Ton CC te guide pour créer le service Railway depuis ton GitHub, te donne la **liste exacte des
variables** à coller (clé Anthropic, ton prénom, ton lien Calendly…), génère l'**URL publique** du
brain, et **teste** que le bot répond dans ta voix.

À la fin, note bien ton **URL Railway** (ex `https://mon-setter.up.railway.app`) — tu en as besoin à l'étape 4.

---

## 🤖 ÉTAPE 4 — Importer la tuyauterie n8n (ton Claude Code)

Colle le prompt **[claude-code/3-import-n8n.md](claude-code/3-import-n8n.md)**.

➡️ Ton CC te guide pour importer le workflow dans n8n, remplir le nœud **Set Keys** (tes clés
Apify/Unipile + ton URL Railway + ton chat Telegram), connecter les credentials OpenAI et Telegram,
brancher le **webhook LinkedIn** côté Unipile, **activer** le workflow et le **tester**.

---

## ✅ ÉTAPE 5 — Tester en réel

Depuis un **autre** compte LinkedIn, envoie-toi un DM. Tu dois voir :
1. une exécution réussie dans n8n (onglet *Executions*),
2. le bot **répondre dans le DM** dans ta voix,
3. (le cas échéant) une **notif Telegram** si le bot passe la main.

🎉 C'est installé.

---

## 🧯 Dépannage rapide

- **Le brain ne démarre pas sur Railway** → vérifie que `ANTHROPIC_API_KEY` est bien mise ET que ton
  compte Anthropic a des **crédits**. Regarde les logs de déploiement Railway.
- **`curl .../` ne répond pas "alive"** → le déploiement n'est pas fini, ou le domaine public n'est pas
  généré (Railway → Settings → Networking → Generate Domain).
- **Le bot répond un truc bizarre / pas dans ta voix** → retourne enrichir `principes.md`,
  `business-info.md` et surtout `objections.md` (plus tu remplis, meilleur il est), puis re-push.
- **n8n : exécution en erreur** → ouvre l'exécution, repère le nœud rouge. 9 fois sur 10 c'est une clé
  manquante dans **Set Keys** ou une **credential** OpenAI/Telegram non connectée.
- **Aucun DM ne déclenche le workflow** → le webhook Unipile ne pointe pas vers la bonne URL n8n, ou le
  workflow n'est pas **activé**.

---

## ⚠️ Règles d'or

- Ne mets **jamais** tes clés API dans un fichier qui part sur GitHub. Le `.env` est déjà ignoré par git.
- Ne donne **aucune** de tes clés à un tiers.
- Commence avec de petits montants de crédits (Anthropic/OpenAI), tu ajusteras selon ton volume.

---

## 📎 Annexe — créer les clés (clic par clic)

**Anthropic** : console.anthropic.com → compte → **Billing** (ajoute des crédits) → **API Keys** →
*Create Key* → copie `sk-ant-...`.

**OpenAI** : platform.openai.com → compte → **Billing** (moyen de paiement + crédits) → **API keys** →
*Create new secret key* → copie `sk-...`.

**Unipile** : unipile.com → compte → dashboard → connecte ton **compte LinkedIn** → dans les réglages
API récupère ta **API key**, ton **DSN** (l'URL de ton instance), ton **Account ID**, et ton
**Provider ID** (l'id de ton profil LinkedIn côté Unipile).

**Apify** : apify.com → compte → **Settings → Integrations → API tokens** → copie le token.

**Telegram** : dans Telegram, écris à **@BotFather** → `/newbot` → suis les étapes → copie le **token**.
(L'id du chat de notif se récupère pendant l'étape 4, ton Claude Code le fait pour toi.)
