# PROMPT 3 — Importer & câbler le workflow n8n
# (à coller dans ton Claude Code, une fois le brain en ligne sur Railway — PROMPT 2 terminé)

Tu m'aides à mettre en place la "tuyauterie" n8n qui relie LinkedIn à mon brain Railway.
Le workflow est dans `n8n/linkedin-dm-setter.template.json`. Guide-moi pas à pas.

## Étape A — Importer le workflow
1. Va sur mon **n8n Cloud** → **Workflows** → bouton **Import from File** (menu "..." en haut à droite).
2. Choisis le fichier `n8n/linkedin-dm-setter.template.json`.
3. Le workflow "LinkedIn DM Setter [Template]" s'ouvre (27 nœuds). Ne l'active PAS encore.

## Étape B — Remplir le nœud "Set Keys" (toute ma config est ici)
Ouvre le nœud **Set Keys** et remplace les placeholders par mes valeurs (rappelle-moi d'où vient chacune) :
- `Apify API Key` → mon token Apify
- `Unipile API Key` → ma clé Unipile
- `Unipile DSN` → mon DSN Unipile (ex `https://apiXXX.unipile.com:XXXXX`)
- `Unipile Account ID` → l'id de mon compte LinkedIn connecté à Unipile
- `My Provider ID` → mon "provider id" LinkedIn (l'id interne de mon profil côté Unipile)
- `Railway Brain URL` → l'URL publique de mon brain Railway (du PROMPT 2, SANS `/chat` à la fin)
- `Telegram Chat ID` → l'id du chat/groupe où je veux recevoir les notifs (voir Étape D)

## Étape B-bis — Mode test vs production (nœud "Paused Profiles")
Le nœud **Paused Profiles** contrôle qui le bot traite :
- `test_allowlist` : **si tu mets des handles ici (séparés par des virgules), le bot ne répondra
  QU'À ces profils** → parfait pour tester sans risque avec un compte à toi. **Vide = production**
  (le bot répond à tout le monde).
- `paused_profiles` : les profils que le bot doit **ignorer** (ex : conversations gérées à la main).

👉 Recommandation : pour les premiers tests, mets le **handle de ton compte de test** dans
`test_allowlist`. Une fois que tout marche, **vide-le** pour passer en production.

## Étape C — Connecter les credentials (2 types)
Certains nœuds ont besoin d'une "credential" n8n (différent des clés du Set Keys) :
1. **OpenAI** — sur les nœuds `Analyze Lead` et `Transcribe Audio` : crée une credential OpenAI
   avec ma clé `sk-...`, et sélectionne-la sur ces 2 nœuds.
2. **Telegram** — sur le nœud `Human Handover` : crée une credential Telegram avec le token de mon
   bot (@BotFather), et sélectionne-la.

## Étape D — Récupérer mon Telegram Chat ID (tu fais le curl)
1. Je m'assure d'avoir écrit un message à mon bot (ou ajouté le bot à mon groupe + envoyé un message).
2. Fais : `curl https://api.telegram.org/bot<MON_TOKEN_BOT>/getUpdates` et trouve le champ
   `chat.id` → c'est mon `Telegram Chat ID` (à remettre dans Set Keys, Étape B).

## Étape E — Brancher le webhook LinkedIn (Unipile → n8n)
1. Ouvre le nœud **Main Webhook** → copie son **Production URL** (se termine par `/linkedin-dm-webhook`).
2. Dans mon dashboard **Unipile**, configure un **webhook** sur les nouveaux messages LinkedIn
   (et réactions) pointant vers cette URL n8n. Guide-moi sur l'écran Unipile exact.

## Étape F — Activer & tester
1. **Active** le workflow (toggle en haut à droite).
2. Depuis un AUTRE compte LinkedIn, envoie-moi un DM.
3. Vérifie : le workflow s'exécute (onglet Executions), le bot répond dans le DM, et je reçois la notif
   Telegram en cas de handover. Si une exécution échoue, ouvre-la avec moi et on lit le nœud en erreur.

## Étape G — Fini 🎉
Quand un DM de test reçoit une réponse correcte du bot, l'installation est complète.
Récapépile-moi : URL Railway, URL webhook n8n, et l'état (actif) du workflow.
