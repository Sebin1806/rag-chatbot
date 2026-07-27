from app.utils.jwt import create_access_token
from app.utils.jwt import verify_access_token

token = create_access_token(
    {"email": "sebin@gmail.com"}
)

print(token)

print(verify_access_token(token))