from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserLogin
from app.utils import hash_password, save_profile_picture
from app.crud import add_user, find_user_by_username, find_user_by_email
from app.auth import authenticate_user
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# GET /signup
@router.get("/signup", response_class=HTMLResponse)
def get_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# POST /signup
@router.post("/signup")
async def signup(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    address_line1: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),
    role: str = Form(...),  # will be converted to role internally
    profile_pic: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Password confirmation check
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Passwords do not match."
        })

    # Check if username or email already exists
    if find_user_by_username(db, username) or find_user_by_email(db, email):
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Username or email already exists."
        })

    # Save profile picture
    profile_pic_path = save_profile_picture(profile_pic)

    # Create UserCreate schema instance (hash password here)
    user_create = UserCreate(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password,  # hashed password
        confirm_password=confirm_password,  # included just for validation completeness
        address_line1=address_line1,
        city=city,
        state=state,
        pincode=pincode,
        role=role,
        profile_pic=profile_pic_path
    )
    user_create.password = hash_password(user_create.password)

    # Add user to DB
    add_user(db, user_create)

    return RedirectResponse(url="/login", status_code=302)


# GET /login
@router.get("/login", response_class=HTMLResponse)
def get_login_form(request: Request):
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse("login.html", {"request": request, "flash": flash})

# POST /login
@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        request.session["flash"] = "Invalid credentials."
        return RedirectResponse(url="/login", status_code=302)

    # Store session
    request.session["user"] = {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }

    print("User logged in:", request.session["user"])  # Debug

    # Redirect based on role
    if user.role.lower() == "patient":
        return RedirectResponse(url="/dashboard/patient", status_code=302)
    else:
        return RedirectResponse(url="/doctor/dashboard", status_code=302)
