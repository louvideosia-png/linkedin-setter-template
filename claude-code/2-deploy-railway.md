# PROMPT 2 — Déployer le brain sur Railway
# (à coller dans ton Claude Code, une fois le PROMPT 1 terminé et ton repo poussé sur GitHub)

Tu m'aides à déployer le "brain" (ce repo) sur Railway. Le repo contient déjà un `Dockerfile`
(qui installe le CLI Claude Code, indispensable) et un `railway.json` qui force Railway à utiliser
ce Dockerfile. Guide-moi pas à pas, et fais toi-même tout ce qui est automatisable.

## Étape A — Pré-vol
1. Vérifie que `Dockerfile` et `railway.json` sont bien présents à la racine, et que `railway.json`
   contient `"dockerfilePath": "Dockerfile"`.
2. Vérifie que mon repo est bien poussé sur GitHub (sinon, commit + push d'abord, JAMAIS le `.env`).

## Étape B — Créer le service Railway (je clique, tu me guides précisément)
Donne-moi les clics exacts :
1. railway.com → **New Project** → **Deploy from GitHub repo**.
2. Autoriser Railway à accéder à mon GitHub si demandé, puis choisir mon repo `mon-setter`.
3. Railway détecte le Dockerfile et lance un premier build (laisse-le finir, il installe Python + le CLI Claude Code, ça peut prendre quelques minutes).

## Étape C — Variables d'environnement (tu me donnes la liste, je colle les valeurs)
Dans le service Railway → onglet **Variables** → **Raw Editor**, je colle ce bloc en remplaçant les valeurs.
Donne-moi EXACTEMENT cette liste à remplir (rappelle-moi d'où vient chaque clé) :

```
ANTHROPIC_API_KEY=        # ma clé console.anthropic.com (OBLIGATOIRE, avec des crédits)
PERSONA_KEY=me
PERSONA_DISPLAY_NAME=     # mon prénom
CALENDLY_URL=            # mon lien de réservation
YOUTUBE_URL=             # optionnel (ma VSL) — laisse vide si aucune
WEBSITE_URL=             # optionnel (mon site offre) — laisse vide si aucun
CLAUDE_MODEL=claude-sonnet-4-6
```

(Ce sont les SEULES variables nécessaires pour le brain. Ne mets pas de clés Unipile/Apify ici :
elles vont dans n8n, pas dans le brain.)

## Étape D — Exposer le service publiquement
1. Service Railway → **Settings** → **Networking** → **Generate Domain** (port 8000 ou celui détecté).
2. Récupère l'URL publique générée (du type `https://xxxx.up.railway.app`).

## Étape E — Vérifier que le brain tourne (tu fais le test)
1. Attends que le déploiement soit "Active".
2. Fais : `curl https://MON-URL.up.railway.app/` → tu dois recevoir un JSON `{"status":"alive", ...}`
   qui liste ma persona et mes tools. Si erreur, regarde les logs de déploiement avec moi.
3. Test de fond : `curl -X POST https://MON-URL.up.railway.app/chat -H "Content-Type: application/json"
   -d '{"last_message":"salut, tu fais quoi dans la vie ?","history":[]}'` → tu dois recevoir une
   réponse rédigée dans ma voix.

## Étape F — Noter l'URL pour la suite
Donne-moi clairement mon **URL publique Railway** : on en aura besoin au PROMPT 3 (câblage n8n),
car c'est l'adresse que n8n appellera. Puis dis-moi : "Brain en ligne — passe au PROMPT 3 (n8n)."
