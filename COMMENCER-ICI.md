# 🚀 COMMENCER ICI — Installer ton chatbot LinkedIn (sans être développeur)

Suis ces étapes **dans l'ordre**. Tu n'écris aucune ligne de code : ton **Claude Code** fait le travail.

---

## ✅ ÉTAPE 1 — Crée tes clés (≈ 30 min, à faire à la main)

Ouvre un bloc-notes, et pour chaque site : crée un compte, puis copie la clé dans ton bloc-notes.

**1. Anthropic** (le cerveau du bot)
- Va sur **console.anthropic.com** → crée ton compte.
- Menu de gauche **Billing** → **Add credits** → mets 20 à 50 €.
- Menu **API Keys** → **Create Key** → copie la clé qui commence par `sk-ant-...`

**2. OpenAI**
- Va sur **platform.openai.com** → crée ton compte.
- **Settings → Billing** → ajoute une carte + un peu de crédits.
- **API keys** → **Create new secret key** → copie la clé `sk-...`

**3. Unipile** (connecte ton LinkedIn)
- Va sur **unipile.com** → crée ton compte → ouvre le **Dashboard**.
- Suis leur assistant pour **connecter ton compte LinkedIn**.
- Copie ta **API Key** et ton **DSN** (l'adresse de ton instance, ex `apiXXX.unipile.com:XXXXX`).
- *(Ton **Account ID** et ton **Provider ID** : pas besoin de les chercher à la main — ton Claude Code les récupérera pour toi plus tard.)*

**4. Apify**
- Va sur **apify.com** → crée ton compte.
- **Settings → Integrations → API tokens** → copie le **token**.

**5. Telegram** (pour recevoir des notifications)
- Dans l'app Telegram, cherche **@BotFather** → écris `/newbot` → suis les questions → copie le **token** du bot.

**6. Crée aussi 3 comptes** (gratuits pour commencer) : **github.com**, **railway.com**, **n8n.io**.

---

## ✅ ÉTAPE 2 — Crée TON dépôt et ouvre-le dans VS Code (10 min)

⚠️ **Ne télécharge PAS le ZIP** : un dossier issu d'un ZIP n'est **pas relié à GitHub**, et la mise en ligne du bot échouera. À la place, on **clone** — VS Code le fait tout seul.

1. Va sur **https://github.com/louvideosia-png/linkedin-setter-template** → bouton vert **« Use this template »** → **Create a new repository** → nom (ex `mon-setter`) → **Private** → **Create repository**. *(Ça crée TA copie sur TON GitHub.)*
2. Sur TON nouveau dépôt, clique le bouton vert **Code** → onglet **HTTPS** → **copie l'adresse** (`https://github.com/TON-COMPTE/mon-setter.git`).
3. Ouvre **VS Code** → appuie sur **`Cmd + Shift + P`** → tape **`Git: Clone`** → **Entrée** → **colle l'adresse** copiée → choisis un dossier où le ranger.
   - Si VS Code te demande de **te connecter à GitHub**, accepte (ça l'autorise à envoyer tes fichiers plus tard).
   - Si VS Code dit que **git n'est pas installé**, clique le lien qu'il propose pour l'installer, puis recommence.
4. Quand VS Code propose **« Ouvrir »** le dépôt cloné → clique **Ouvrir**.

✅ Ton projet est ouvert dans VS Code, **connecté à ton GitHub**.

---

## ✅ ÉTAPE 3 — Lance Claude Code

*(Pas encore Claude Code ? Installe l'extension Claude Code dans VS Code, ou l'app officielle d'Anthropic.)*

- Dans VS Code, ouvre **Claude Code** (l'extension) : il travaille déjà dans ton dossier. C'est tout.
- *(Si tu utilises Claude Code en ligne de commande : dans VS Code, menu **Terminal → New Terminal**, puis tape **`claude`**.)*

---

## ✅ ÉTAPE 4 — Donne les 3 instructions, une par une

Dans Claude Code, **écris ces phrases une par une**. Attends que chacune soit complètement finie avant de passer à la suivante. Claude Code te posera des questions — réponds simplement.

**Instruction 1 :**
> Lis le fichier `claude-code/1-install.md` et suis-le étape par étape pour personnaliser mon bot avec mon business.

**Instruction 2 :**
> Lis le fichier `claude-code/2-deploy-railway.md` et suis-le pour mettre mon bot en ligne sur Railway.

**Instruction 3 :**
> Lis le fichier `claude-code/3-import-n8n.md` et suis-le pour brancher mon bot à mon LinkedIn via n8n.

---

## ✅ ÉTAPE 5 — Teste

Depuis un **autre** compte LinkedIn, envoie-toi un message privé. Ton bot doit répondre tout seul. 🎉

> 💡 Astuce : pour tes premiers tests, demande à Claude Code de mettre **ton compte de test** dans la
> "test_allowlist" (il sait ce que c'est) — comme ça le bot ne répond qu'à toi le temps de vérifier.

---

## 🆘 Si tu bloques
Dis simplement à ton Claude Code ce qui se passe (copie-lui le message d'erreur), il t'aide à corriger.
Les soucis les plus fréquents : crédits Anthropic vides, une clé oubliée, ou le workflow n8n pas activé.
