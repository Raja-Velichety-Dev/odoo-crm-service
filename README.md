# CRM Server (Odoo Integration)

This project is a server setup for interacting with Odoo, containerized using Docker. It is designed for local development and production deployment.

## URLs

**Local:**  
- Odoo UI: `http://localhost:8069/web`  
- API Docs: `http://localhost:8000/docs`  

**Relative:**  
- Odoo UI: `/web`  
- API Docs: `/docs`  

## Configuration

- Create a `.env` file with your Odoo credentials and DB info.  
- Do **not** commit sensitive information.  

## Quick Start (Development)

```bash
cd crm
docker compose up --build
```
