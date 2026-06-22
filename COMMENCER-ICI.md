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

## ✅ ÉTAPE 2 — Crée TON dépôt et installe-le sur ton ordi (10 min)

⚠️ **Important** : ton dossier doit rester **connecté à GitHub** (sinon la mise en ligne échouera plus tard). On utilise donc **GitHub Desktop**, une appli gratuite avec des boutons (pas de code). **Ne télécharge PAS le ZIP** : ça déconnecte le dossier de GitHub et le bot ne marchera pas.

1. Va sur **https://github.com/louvideosia-png/linkedin-setter-template** → bouton vert **« Use this template »** → **Create a new repository** → nom (ex `mon-setter`) → **Private** → **Create repository**. *(Ça crée TA copie du template sur TON GitHub.)*
2. Installe **GitHub Desktop** : va sur **desktop.github.com** → **Download** → installe → **connecte-toi avec ton compte GitHub**.
3. Dans GitHub Desktop : menu **File → Clone repository** → onglet **GitHub.com** → choisis ton dépôt `mon-setter` → **Clone**. *(Note le "Local Path" affiché, souvent `Documents/GitHub/mon-setter`.)*

✅ Tu as maintenant un dossier `mon-setter` sur ton ordi, **connecté à ton GitHub**.

---

## ✅ ÉTAPE 3 — Ouvre Claude Code dans ce dossier

*(Pas encore Claude Code ? Installe-le d'abord : cherche "Claude Code download" sur Google et suis l'installation officielle d'Anthropic.)*

1. Dans **GitHub Desktop**, ton dépôt étant ouvert : menu **Repository → Open in Terminal**.
   → une fenêtre noire s'ouvre, **déjà placée dans le bon dossier**.
2. Dans cette fenêtre, tape **`claude`** puis **Entrée**. ✅ Claude Code démarre dans ton dossier.

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
