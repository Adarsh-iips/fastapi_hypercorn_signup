from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.crud import find_user_by_username, get_doctor_blogs, create_blog
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BlogCreate
from uuid import uuid4
import os
from app.models import User, BlogPost
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard/patient", response_class=HTMLResponse)
def patient_dashboard(request: Request, db: Session = Depends(get_db)):
    session_user = request.session.get("user")
    if not session_user or session_user["role"].lower() != "patient":
        return RedirectResponse(url="/login", status_code=302)
    
    # Get all published blog posts
    blogs = db.query(BlogPost).filter(BlogPost.is_draft == False).all()
    
    # Ensure category keys are pre-defined
    categories = ["Mental Health", "Heart Disease", "Covid-19", "Immunization"]
    categorized_blogs = {category: [] for category in categories}

    # Sort blogs into categories
    for blog in blogs:
        if blog.category in categorized_blogs:
            categorized_blogs[blog.category].append(blog)

    user = find_user_by_username(db, session_user["username"])

    return templates.TemplateResponse("patient_dashboard.html", {
        "request": request,
        "user": user,
        "categorized_blogs": categorized_blogs  # <- FIXED missing comma
    })


@router.get("/doctor/dashboard", response_class=HTMLResponse)
def doctor_dashboard(request: Request, db: Session = Depends(get_db)):
    session_user = request.session.get("user")
    if not session_user or session_user["role"].lower() != "doctor":
        return RedirectResponse(url="/login", status_code=302)

    user = find_user_by_username(db, session_user["username"])
    blogs = get_doctor_blogs(db, doctor_id=user.id)

    return templates.TemplateResponse("doctor_dashboard.html", {
        "request": request,
        "user": user,
        "blogs": blogs
    })


@router.get("/doctor/blog/create", response_class=HTMLResponse)
def create_blog_form(request: Request):
    session_user = request.session.get("user")
    if not session_user or session_user["role"] != "Doctor":
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("create_blog.html", {"request": request, "user": session_user})

@router.post("/doctor/blog/create", response_class=HTMLResponse)
async def submit_blog_form(
    request: Request,
    title: str = Form(...),
    image_url: UploadFile = File(...),
    category: str = Form(...),
    summary: str = Form(...),
    content: str = Form(...),
    is_draft: bool = Form(False),
    db: Session = Depends(get_db),
):
    session_user = request.session.get("user")
    if not session_user or session_user["role"] != "Doctor":
        return RedirectResponse("/login", status_code=302)

    user = find_user_by_username(db, session_user["username"])

    # Save the uploaded image
    image_filename = f"{uuid4().hex}_{image_url.filename}"
    image_path = f"static/blog_images/{image_filename}"

    # Ensure directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    with open(image_path, "wb") as f:
        f.write(await image_url.read())

    # Create blog data
    blog_data = BlogCreate(
        title=title,
        image_url=f"/{image_path}",  # accessible via /static/...
        category=category,
        summary=summary,
        content=content,
        is_draft=is_draft
    )

    create_blog(db, blog_data, doctor_id=user.id)

    return RedirectResponse("/doctor/dashboard", status_code=302)
