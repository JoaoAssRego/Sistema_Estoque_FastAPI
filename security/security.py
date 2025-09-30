from passlib.context import CryptContext

# Configure CryptContext with bcrypt
bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__default_rounds=12  # You can adjust the rounds for security/performance
)