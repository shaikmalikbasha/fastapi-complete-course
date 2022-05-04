from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(raw_text: str) -> str:
    return pwd_context.hash(raw_text)


def verify(plain, hashed):
    return pwd_context.verify(plain, hashed)
