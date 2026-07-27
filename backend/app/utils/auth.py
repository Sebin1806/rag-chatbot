from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from app.utils.jwt import verify_access_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    print("\n========== AUTH DEBUG ==========")
    print("Scheme:", credentials.scheme)
    print("Token:", credentials.credentials)

    payload = verify_access_token(credentials.credentials)

    print("Payload:", payload)
    print("================================\n")

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    return payload