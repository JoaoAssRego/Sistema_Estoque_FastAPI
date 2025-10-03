from passlib.context import CryptContext
import os
from dotenv import load_dotenv
# Configure CryptContext with bcrypt
bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__default_rounds=12  # You can adjust the rounds for security/performance
)

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))