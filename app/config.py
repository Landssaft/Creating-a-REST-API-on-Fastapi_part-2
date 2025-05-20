import os



POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology")

PG_DSN = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


TOKEN_TTL_SEC = os.getenv("TOKEN_TTL", 60 * 60 * 24 * 2)