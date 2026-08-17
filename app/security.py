import os
import time

import bcrypt
import jwt

from dotenv import load_dotenv


load_dotenv()


MEDCARE_SECRET_KEY = os.getenv(
    "MEDCARE_SECRET_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "20"
    )
)

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed.decode("utf-8")


def verify_password(
    password: str,
    hashed_password: str
) -> bool:

    password_bytes = password.encode("utf-8")

    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hashed_bytes
    )

def create_access_token(
    username: str,
    role: str
) -> str:

    issued_at = int(time.time())

    expires_at = (
        issued_at
        + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    payload = {
        "sub": username,
        "role": role,
        "iat": issued_at,
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        MEDCARE_SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_access_token(token: str):

    payload = jwt.decode(
        token,
        MEDCARE_SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload