from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

SENDER_EMAIL = config("SENDER_EMAIL")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")
SECRET_KEY = config("SECRET_KEY")
DATABASE_URL=config("DATABASE_URL", cast=Secret)
SECRET_KEY_token = config("SECRET_KEY_token")
ALGORITHM  = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=config("ACCESS_TOKEN_EXPIRE_MINUTES")
SMTP_SERVER = config("SMTP_SERVER")
SMTP_PORT=config("SMTP_PORT")