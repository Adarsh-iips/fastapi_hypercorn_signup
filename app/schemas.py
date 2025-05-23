from pydantic import BaseModel, EmailStr, field_validator, model_validator
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
    role: str  # consistent with models.py

    model_config = {
        "from_attributes": True  # Pydantic v2 equivalent of `orm_mode`
    }


class UserCreate(UserBase):
    password: str
    confirm_password: str
    profile_pic: Optional[str] = None  # e.g., path or URL string

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = {
        "from_attributes": True
    }

class BlogCreate(BaseModel):
    title: str
    image_url: str
    category: str
    summary: str
    content: str
    is_draft: bool

class BlogOut(BlogCreate):
    id: int
    doctor_id: int

    class Config:
        orm_mode = True
