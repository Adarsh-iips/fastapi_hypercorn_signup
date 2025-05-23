from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(10))  # doctor or patient
    address_line1 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(20))
    profile_pic = Column(String(255), nullable=True)

    blog_posts = relationship("BlogPost", back_populates="doctor")


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    image_url = Column(String(255))  # Store image filename or URL
    category = Column(String(50), nullable=False)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    is_draft = Column(Boolean, default=False)
    doctor_id = Column(Integer, ForeignKey("users.id"))
