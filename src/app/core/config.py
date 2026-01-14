from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe de configuration qui charge les variables d'environnement.
    """
    # Configuration du modèle Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True  # Respecte la casse des variables
    )

    SEED_DATABASE: bool = True

    # Paramètres du projet
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_STR: str = "/api/v1"

    # Configuration de la base de données
    # Le type hint `str` est suffisant, mais des types plus stricts peuvent être utilisés
    DATABASE_URL: str = "sqlite+aiosqlite:///./local_dev.db"

    # Configuration de la sécurité (JWT)
    # SECRET_KEY: str
    # ALGORITHM: str = "HS256"
    #ACCESS_TOKEN_EXPIRE_MINUTES: int = 30



# Création d'une instance unique des paramètres qui sera importée dans le reste de l'application
settings = Settings()