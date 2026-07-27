from jose import jwt
from jose import JWTError
from datetime import datetime
from datetime import timedelta


SECRET_KEY = "your_super_secret_key_change_this"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    print("\n========== TOKEN CREATED ==========")
    print(token)
    print("===================================\n")

    return token


def verify_access_token(token: str):

    try:

        print("\n========== VERIFY TOKEN ==========")
        print("Received Token:")
        print(token)

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("\nDecoded Payload:")
        print(payload)

        print("==================================\n")

        return payload

    except JWTError as e:

        print("\n========== JWT ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("===============================\n")

        return None