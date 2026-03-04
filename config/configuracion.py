from pydantic_settings import BaseSettings, SettingsConfigDict

class Constantes(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    # Esta es la sintaxis moderna para Pydantic V2
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Constantes()