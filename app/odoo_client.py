import random
import httpx
from fastapi import HTTPException
from loguru import logger
from .config import settings

class OdooClient:
    def __init__(self):
        self._client = httpx.Client(timeout=15)
        self._uid = None

    def _jsonrpc(self, payload):
        response = self._client.post(f"{settings.ODOO_URL}/jsonrpc", json=payload)
        response.raise_for_status()
        return response.json()

    def authenticate(self):
        auth_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [settings.ODOO_DB_NAME, settings.ODOO_USERNAME, settings.ODOO_PASSWORD, {}],
            },
            "id": random.randint(0, 1000000000),
        }
        result = self._jsonrpc(auth_payload).get("result")
        if not result:
            raise HTTPException(status_code=401, detail="Authentication failed")
        self._uid = result
        logger.info(f"Authenticated with UID {self._uid}")

    def find_partner_by_email(self, email):
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    settings.ODOO_DB_NAME, self._uid, settings.ODOO_PASSWORD,
                    "res.partner", "search_read",
                    [[["email", "=", email]]],
                    {"fields": ["id", "name", "email"], "limit": 1}
                ],
            },
            "id": random.randint(0, 1000000000),
        }
        result = self._jsonrpc(payload).get("result")
        return result[0] if result else None

    def create_partner(self, name, email):
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    settings.ODOO_DB_NAME, self._uid, settings.ODOO_PASSWORD,
                    "res.partner", "create",
                    [{"name": name, "email": email}]
                ],
            },
            "id": random.randint(0, 1000000000),
        }
        return self._jsonrpc(payload).get("result")

    def create_lead(self, partner_id, name, email, summary):
        lead_data = {
            "name": f"Lead: {name}",
            "contact_name": name,
            "email_from": email,
            "partner_id": partner_id,
            "description": summary,
        }
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    settings.ODOO_DB_NAME, self._uid, settings.ODOO_PASSWORD,
                    "crm.lead", "create", [lead_data]
                ],
            },
            "id": random.randint(0, 1000000000),
        }
        return self._jsonrpc(payload).get("result")
