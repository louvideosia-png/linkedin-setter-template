# PROMPT 1 — Installation & remplissage du brain
# (copie-colle TOUT ce bloc dans ton Claude Code, ouvert dans le dossier du dépôt)

Tu es mon assistant d'installation pour ce template de chatbot LinkedIn "appointment setter".
Le code (moteur) est déjà là et ne doit PAS être modifié. Ton job : m'aider à le PERSONNALISER
pour mon business, puis préparer le déploiement. Procède dans cet ordre, en attendant ma validation
à chaque étape.

## Étape A — Vérifier l'environnement (IMPORTANT)
1. Confirme que tu vois bien `main.py`, `config.py`, `.env.example` et le dossier `prompts/`.
2. **Vérifie que ce dossier est bien un clone git connecté à mon GitHub** : lance `git remote -v`.
   - Si ça affiche une URL `github.com/.../mon-setter` → parfait, continue.
   - Si ça n'affiche RIEN (ou erreur "not a git repository") → **STOP**. Ça veut dire que le dossier
     vient d'un ZIP, pas d'un clone. Dans ce cas, dis-moi clairement de refaire l'ÉTAPE 2 du guide
     avec **GitHub Desktop (Clone repository)**, sinon la mise en ligne (PROMPT 2) déploiera un bot vide.
3. Liste-moi tous les fichiers qui contiennent le marqueur `🟨` (ce sont ceux que je dois remplir).

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

## Étape D — Test local du brain (OPTIONNEL)
Ce test est facultatif. **Si l'installation Python pose le moindre souci, SAUTE cette étape** : on
testera le bot directement en ligne au PROMPT 2 (c'est aussi fiable).
1. Si on tente : crée un venv, installe `requirements.txt`, lance `uvicorn main:app --port 8000`.
2. `curl localhost:8000/` doit répondre status "alive" + lister ma persona.
3. Un appel test sur `/chat` doit renvoyer une réponse dans ma voix. Sinon, on ajuste les fichiers 🟨.
Si quoi que ce soit bloque ici → on passe directement à l'étape E, ce n'est pas grave.

## Étape E — Commit & push (OBLIGATOIRE pour la suite)
1. Commit TOUS les fichiers remplis — mais **JAMAIS le `.env`** (vérifie qu'il est dans `.gitignore`).
2. Pousse sur mon dépôt GitHub : `git push`.
3. **Si le push échoue** (souci d'authentification) : dis-moi d'ouvrir **GitHub Desktop** et de cliquer
   **« Push origin »** en haut à droite — ça enverra les fichiers. Le push DOIT réussir avant le PROMPT 2,
   sinon Railway déploiera la version vide.

Quand le push est confirmé sur GitHub, dis-moi : "Brain prêt — passe au PROMPT 2 (déploiement Railway)."
