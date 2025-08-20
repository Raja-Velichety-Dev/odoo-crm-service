from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ODOO_URL: str
    ODOO_DB_NAME: str
    ODOO_USERNAME: str
    ODOO_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()