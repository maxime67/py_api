from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe de configuration qui charge les variables d'environnement.
    Toutes les variables peuvent être surchargées via l'environnement pour Kubernetes.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # Environnement d'exécution
    ENVIRONMENT: str = "development"

    # Paramètres du projet
    PROJECT_NAME: str = "API Filmothèque"
    API_V1_STR: str = "/api/v1"

    # Configuration du serveur
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    LOG_LEVEL: str = "info"

    # Configuration de la base de données
    DATABASE_URL: str = "sqlite+aiosqlite:///./local_dev.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_RECYCLE: int = 3600

    # Configuration du seeding
    SEED_DATABASE: bool = True


settings = Settings()