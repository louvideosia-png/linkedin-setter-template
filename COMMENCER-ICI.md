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
- Dans les réglages, copie ces 4 infos : **API Key**, **DSN**, **Account ID**, **Provider ID**.

**4. Apify**
- Va sur **apify.com** → crée ton compte.
- **Settings → Integrations → API tokens** → copie le **token**.

**5. Telegram** (pour recevoir des notifications)
- Dans l'app Telegram, cherche **@BotFather** → écris `/newbot` → suis les questions → copie le **token** du bot.

**6. Crée aussi 3 comptes** (gratuits pour commencer) : **github.com**, **railway.com**, **n8n.io**.

---

## ✅ ÉTAPE 2 — Récupère le template (5 min)

1. Va sur **https://github.com/louvideosia-png/linkedin-setter-template**.
2. Clique le bouton vert **« Use this template »** → **Create a new repository**.
3. Donne un nom (ex : `mon-setter`), choisis **Private**, clique **Create repository**.
4. Sur ton nouveau dépôt, clique **Code** (bouton vert) → **Download ZIP**.
5. **Dézippe** le fichier sur ton ordinateur (double-clic).

---

## ✅ ÉTAPE 3 — Ouvre Claude Code dans ce dossier

1. Ouvre **Claude Code**.
2. Mets-le dans le dossier que tu viens de dézipper *(glisse le dossier dessus, ou ouvre-le)*.

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
