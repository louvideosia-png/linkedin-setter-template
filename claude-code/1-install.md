# PROMPT 1 — Installation & remplissage du brain
# (copie-colle TOUT ce bloc dans ton Claude Code, ouvert dans le dossier du dépôt)

Tu es mon assistant d'installation pour ce template de chatbot LinkedIn "appointment setter".
Le code (moteur) est déjà là et ne doit PAS être modifié. Ton job : m'aider à le PERSONNALISER
pour mon business, puis préparer le déploiement. Procède dans cet ordre, en attendant ma validation
à chaque étape.

## Étape A — Vérifier l'environnement
1. Confirme que tu vois bien `main.py`, `config.py`, `.env.example` et le dossier `prompts/`.
2. Liste-moi tous les fichiers qui contiennent le marqueur `🟨` (ce sont ceux que je dois remplir).
3. Vérifie que Python 3.12+ est disponible (`python3 --version`).

## Étape B — Remplir les fichiers de mon business (le cœur)
Pour CHAQUE fichier 🟨 ci-dessous, dans cet ordre, tu m'INTERVIEWES en français avec des questions
simples et concrètes, puis tu RÉDIGES le contenu à ma place, et tu me le montres pour validation avant
d'écrire. Ne laisse aucun `{{...}}` ni `🟨` non résolu.

1. `prompts/personas/me.md` — mon identité (nom, genre, ville, handle LinkedIn, mon positionnement).
2. `prompts/skills/business-info.md` — mon offre : ce que je vends, à qui, le mécanisme, mes chiffres
   réels, mes garanties, les distinctions de mon offre, les questions pièges + mes réponses.
3. `prompts/skills/objections.md` — les objections que j'entends VRAIMENT, et pour chacune ma meilleure
   réponse. Aide-moi à en lister un maximum (interroge-moi marché par marché).
4. `prompts/skills/bio-detail.md` — mon parcours, mes preuves sociales, ce que je révèle ou pas.
5. `prompts/principes.md` — remplis UNIQUEMENT les zones 🟨 (la section "Ce que je vends", mon point
   d'ancrage, mes interdits, ma réponse "es-tu une IA ?"). NE TOUCHE PAS au reste (méthodo générique).
6. `prompts/skills/phase-2-acquisition.md` et `phase-3-asset.md` — adapte les quelques zones 🟨
   (mon axe de questions, mes pains, mes assets de valeur).

Règle d'or : tu ne dois JAMAIS inventer un chiffre, une preuve ou une promesse. Si je ne te donne pas
l'info, mets une formulation prudente ("on en parle en call") plutôt qu'une invention.

## Étape C — Configurer les clés
1. Copie `.env.example` en `.env`.
2. Demande-moi mes clés une par une et remplis le `.env` :
   - `ANTHROPIC_API_KEY`, `PERSONA_DISPLAY_NAME` (mon prénom),
   - `CALENDLY_URL`, et si j'en ai `YOUTUBE_URL` / `WEBSITE_URL`.
3. Rappelle-moi que `.env` ne doit jamais être commité (vérifie qu'il est bien dans `.gitignore`).

## Étape D — Test local du brain
1. Crée un venv, installe `requirements.txt`.
2. Lance `uvicorn main:app --port 8000` et fais un appel test :
   `curl localhost:8000/` (doit répondre status "alive" + lister ma persona).
3. Fais un appel de test sur `/chat` avec un faux message de prospect et montre-moi la réponse du bot.
   Si la réponse ne ressemble pas à ma voix, on retourne ajuster les fichiers 🟨.

## Étape E — Commit & push
Quand je valide, commit les fichiers remplis (PAS le `.env`) et pousse sur mon dépôt GitHub.

Quand tout est vert, dis-moi : "Brain prêt — passe au PROMPT 2 (déploiement Railway)."
