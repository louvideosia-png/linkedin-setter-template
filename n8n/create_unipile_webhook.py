#!/usr/bin/env python3
"""Crée (de façon autonome et reproductible) le webhook Unipile qui relie LinkedIn à n8n.

Ce script NE dépend d'AUCUN webhook préexistant : le schéma du payload (les champs que
Unipile envoie à n8n) est écrit en dur ci-dessous, identique à celui qu'attend le workflow
`linkedin-dm-setter.template.json` (nœuds Normalize Webhook / Not My Message? / Is Paused?).

Usage (renseigne les 4 variables d'environnement, puis lance) :

    export UNIPILE_DSN="https://apiXXX.unipile.com:XXXXX"     # ton DSN Unipile
    export UNIPILE_API_KEY="..."                              # ta clé API Unipile
    export UNIPILE_ACCOUNT_ID="..."                           # l'id du compte LinkedIn (via /api/v1/accounts)
    export N8N_WEBHOOK_URL="https://<ton-n8n>/webhook/linkedin-dm-webhook"  # Production URL du nœud Main Webhook
    python3 n8n/create_unipile_webhook.py

Pour trouver UNIPILE_ACCOUNT_ID :
    curl -H "X-API-KEY: $UNIPILE_API_KEY" "$UNIPILE_DSN/api/v1/accounts"
    -> repère ton compte LINKEDIN, son champ `id` = UNIPILE_ACCOUNT_ID.
"""

import os
import json
import sys
import urllib.request
import urllib.error

# Les champs natifs d'un webhook "messaging" Unipile, tels qu'attendus par le workflow n8n.
# (clé = nom => on transmet le payload natif tel quel)
DATA_FIELDS = [
    "account_id", "account_type", "account_info", "webhook_name", "chat_id",
    "attendees", "sender", "subject", "message", "message_id", "timestamp",
    "attachments", "reaction", "reaction_sender", "read_by", "is_sender",
    "provider_chat_id", "provider_message_id", "is_event", "chat_pinned",
    "quoted", "is_forwarded", "chat_content_type", "message_type", "is_group", "folder",
]


def main():
    dsn = os.environ.get("UNIPILE_DSN", "").rstrip("/")
    key = os.environ.get("UNIPILE_API_KEY", "")
    account_id = os.environ.get("UNIPILE_ACCOUNT_ID", "")
    n8n_url = os.environ.get("N8N_WEBHOOK_URL", "")

    missing = [n for n, v in [
        ("UNIPILE_DSN", dsn), ("UNIPILE_API_KEY", key),
        ("UNIPILE_ACCOUNT_ID", account_id), ("N8N_WEBHOOK_URL", n8n_url),
    ] if not v]
    if missing:
        sys.exit("Variables d'environnement manquantes : " + ", ".join(missing))

    body = {
        "source": "messaging",
        "request_url": n8n_url,
        "name": "linkedin-dm-setter-railway",
        "format": "json",
        "enabled": True,
        "events": ["message_received", "message_reaction"],
        "account_ids": [account_id],
        "headers": [{"key": "Content-Type", "value": "application/json"}],
        "data": [{"key": f, "name": f} for f in DATA_FIELDS],
    }

    req = urllib.request.Request(
        f"{dsn}/api/v1/webhooks",
        data=json.dumps(body).encode(),
        headers={"X-API-KEY": key, "accept": "application/json", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            res = json.load(r)
        print("✅ Webhook Unipile créé :", json.dumps(res))
    except urllib.error.HTTPError as e:
        sys.exit(f"❌ Erreur {e.code} : {e.read().decode()[:600]}")


if __name__ == "__main__":
    main()
