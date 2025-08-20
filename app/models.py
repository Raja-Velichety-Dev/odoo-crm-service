from pydantic import BaseModel

class LeadRequest(BaseModel):
    client_name: str
    email: str
    summary: str

class LeadResponse(BaseModel):
    lead_id: int
    partner_id: int
    message: str
