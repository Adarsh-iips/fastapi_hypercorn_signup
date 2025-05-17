import os
import shutil
from passlib.context import CryptContext
from uuid import uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def save_profile_picture(upload_file, upload_dir="static/profile_pics") -> str:
    ext = os.path.splitext(upload_file.filename)[1]
    unique_name = f"{uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, unique_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path.replace("\\", "/")  # for compatibility on Windows
