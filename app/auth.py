from app.utils import verify_password
from app.database import find_user_by_username

def authenticate_user(username: str, password: str):
    user = find_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user
