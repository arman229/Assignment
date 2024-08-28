from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

SENDER_EMAIL = config("SENDER_EMAIL")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")
SECRET_KEY = config("SECRET_KEY")
 
