# 🤖 PROMPT TOUT-EN-UN — Installe mon chatbot LinkedIn de A à Z
# (Ouvre Claude Code dans un dossier VIDE, puis colle TOUT ce bloc. Claude Code fait le reste.)

Tu es mon installateur autonome. Tu vas installer un chatbot d'appointment setting LinkedIn pour MON
business, en automatisant TOUT ce qui peut l'être. Tu procèdes phase par phase, tu attends ma validation
entre les phases, et tu ne me fais cliquer que quand c'est techniquement impossible autrement.

Avant de commencer, vérifie avec moi que j'ai déjà créé mes comptes et mes clés. Si je n'ai pas encore
une clé, arrête-toi et dis-moi exactement où la créer. Les clés/comptes nécessaires :
- **Anthropic** (clé `sk-ant-...` + des crédits) — le cerveau du bot
- **OpenAI** (clé `sk-...` + crédits) — analyse + transcription
- **Unipile** (API Key + DSN) + mon **LinkedIn déjà connecté** dans le dashboard Unipile
- **Apify** (token)
- **Telegram** (token de bot via @BotFather)
- **Railway** (compte créé + un **token** : railway.com → Account Settings → Tokens)
- **n8n Cloud** (compte créé + une **API key** : Settings → n8n API)
- **GitHub** (compte + un **token classic avec scope `repo`** : Settings → Developer settings → Tokens classic)

Demande-moi ces valeurs au fur et à mesure (je te les colle ici). Ne les écris JAMAIS dans un fichier
qui sera commité (uniquement dans `.env` local et dans les dashboards Railway/n8n).

---

## PHASE 1 — Récupérer le template
1. Clone le template public DANS le dossier courant :
   `git clone https://github.com/louvideosia-png/linkedin-setter-template.git .`
   (le point final = "ici"). Si le dossier n'est pas vide, préviens-moi.
2. Confirme que tu vois `main.py`, `prompts/`, `n8n/`, `claude-code/`.

## PHASE 2 — Personnaliser le brain (mon business)
Suis le détail du fichier `claude-code/1-install.md`, sections "Remplir les fichiers" :
tu m'INTERVIEWES en français, tu rédiges, je valide, et tu remplis TOUS les fichiers `🟨`
(`prompts/personas/me.md`, `business-info.md`, `objections.md`, `bio-detail.md`, les zones 🟨 de
`principes.md`, `phase-2`, `phase-3`). Ne laisse aucun `{{...}}` ni `🟨`. N'invente jamais un chiffre.

## PHASE 3 — Mettre le code sur MON GitHub
1. Demande-moi mon **token GitHub**.
2. Crée un dépôt privé sur mon compte via l'API GitHub (nom `mon-setter-bot`).
3. Initialise git ici, mets mon `.env` dans `.gitignore` (vérifie qu'il y est), commit tout SAUF le
   `.env`, et pousse sur ce dépôt.

## PHASE 4 — Déployer le brain sur Railway (automatisé)
Suis `claude-code/2-deploy-railway.md` mais en AUTOMATISANT via le Railway CLI :
1. Demande-moi mon **token Railway**.
2. Installe le CLI si besoin (`npm i -g @railway/cli`, ou utilise `npx @railway/cli`).
3. Avec `RAILWAY_TOKEN`, crée un projet + service, déploie ce dossier (`railway up`), et définis les
   variables : `ANTHROPIC_API_KEY`, `PERSONA_KEY=me`, `PERSONA_DISPLAY_NAME` (mon prénom),
   `CALENDLY_URL`, `YOUTUBE_URL`/`WEBSITE_URL` si j'en ai, `CLAUDE_MODEL=claude-sonnet-4-6`.
4. Génère un domaine public, attends que ce soit "Active", puis teste :
   `curl https://MON-URL/` doit répondre `{"status":"alive"...}`. Donne-moi l'URL publique.
   - ⚠️ Si une étape exige une autorisation dans le navigateur Railway, dis-moi précisément quoi cliquer.

## PHASE 5 — Brancher la tuyauterie n8n (automatisé via l'API n8n)
Suis `claude-code/3-import-n8n.md` mais en AUTOMATISANT :
1. Demande-moi mon **API key n8n** et l'URL de mon n8n Cloud.
2. Importe `n8n/linkedin-dm-setter.template.json` via l'API n8n (POST /api/v1/workflows).
3. Remplis le nœud **Set Keys** : `Apify API Key`, `Unipile API Key`, `Unipile DSN`,
   `Railway Brain URL` (l'URL Railway de la phase 4), `Telegram Chat ID`.
4. Récupère TOI-MÊME mon `Unipile Account ID` et `My Provider ID` via l'API Unipile
   (`curl -H "X-API-KEY: MA_CLE" "https://MON_DSN/api/v1/accounts"`) et remplis-les dans Set Keys.
5. Crée les credentials n8n OpenAI (nœuds `Analyze Lead`, `Transcribe Audio`) et Telegram
   (`Human Handover`) via l'API n8n, avec mes clés.
6. Récupère mon `Telegram Chat ID` : `curl https://api.telegram.org/bot<MON_TOKEN>/getUpdates`
   (après que j'aie écrit un message à mon bot) → remplis-le dans Set Keys.

## PHASE 6 — Relier LinkedIn → n8n (webhook Unipile)
1. Récupère l'URL de production du webhook n8n (le nœud `Main Webhook`, finit par `/linkedin-dm-webhook`).
2. Crée le webhook côté Unipile **avec le script fourni** `n8n/create_unipile_webhook.py` (il contient
   déjà le bon schéma de payload — NE copie PAS un webhook existant, ça ne serait pas reproductible) :
   ```
   export UNIPILE_DSN="https://apiXXX.unipile.com:XXXXX"
   export UNIPILE_API_KEY="MA_CLE_UNIPILE"
   export UNIPILE_ACCOUNT_ID="MON_ACCOUNT_ID"   # l'id du compte LinkedIn (cf. Phase 5, /api/v1/accounts)
   export N8N_WEBHOOK_URL="https://MON-N8N/webhook/linkedin-dm-webhook"
   python3 n8n/create_unipile_webhook.py
   ```
   Le webhook créé écoute `message_received` + `message_reaction` sur MON compte LinkedIn et pointe vers n8n.
   Si l'API Unipile bloque, donne-moi les clics exacts à faire dans le dashboard Unipile.

## PHASE 7 — Mode test, activation, vérification
1. Mets MON compte de test dans le champ `test_allowlist` du nœud `Paused Profiles` (le bot ne
   répondra qu'à moi le temps du test). Active le workflow via l'API n8n.
2. Demande-moi d'envoyer un DM de test depuis un autre compte LinkedIn.
3. Vérifie l'exécution n8n (via l'API) et confirme avec moi que le bot a répondu dans ma voix.
4. Quand c'est bon : vide `test_allowlist` pour passer en production. Fais-moi un récap final
   (URL Railway, workflow n8n actif, et les clés à révoquer si je veux faire le ménage).

---

⚠️ Règles : ne commit jamais une clé. Demande-moi chaque clé au moment où tu en as besoin (pas toutes
d'un coup). Si une API te bloque, explique-moi simplement quoi faire et continue dès que c'est débloqué.
