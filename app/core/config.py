import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    settings for fastapi stuff, make sure to add fallback in case env fails to load
    """
    # DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/test_db")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-stuff-for-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Caching
    CACHE_TTL_MINUTES: int = int(os.getenv("CACHE_TTL_MINUTES", 5))

    # Payload Size Limit for AddPost (in bytes)
    MAX_PAYLOAD_SIZE_MB: int = int(os.getenv("MAX_PAYLOAD_SIZE_MB", 1))
    MAX_PAYLOAD_SIZE_BYTES: int = MAX_PAYLOAD_SIZE_MB * 1024 * 1024


settings = Settings()