from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    address_line1: str
    city: str
    state: str
    pincode: str
    user_type: str

class UserCreate(UserBase):
    password: str
    confirm_password: str
    profile_pic: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
