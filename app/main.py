from fastapi import FastAPI, HTTPException
from loguru import logger
from .models import LeadRequest, LeadResponse
from .odoo_client import OdooClient

app = FastAPI(title="CRM API", description="API to manage CRM leads in Odoo")

@app.post("/crm/lead", response_model=LeadResponse)
def create_crm_lead(request: LeadRequest):
    client = OdooClient()
    client.authenticate()

    # Check if partner exists
    partner = client.find_partner_by_email(request.email)
    if partner:
        partner_id = partner["id"]
        logger.info(f"Found existing partner {partner_id}")
    else:
        partner_id = client.create_partner(request.client_name, request.email)
        logger.info(f"Created new partner {partner_id}")

    # Create lead
    lead_id = client.create_lead(partner_id, request.client_name, request.email, request.summary)
    if not lead_id:
        raise HTTPException(status_code=500, detail="Failed to create lead")
    logger.success(f"Created lead with ID {lead_id}")
    return LeadResponse(
        lead_id=lead_id,
        partner_id=partner_id,
        message="Lead and partner data added successfully"
    )
