from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.schemas import UserCreate, UserLogin
from app.utils import hash_password, save_profile_picture
from app.database import add_user, find_user_by_username, find_user_by_email
from app.auth import authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/signup", response_class=HTMLResponse)
def get_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

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
    user_type: str = Form(...),
    profile_pic: UploadFile = File(...)
):
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Passwords do not match."
        })

    if find_user_by_username(username) or find_user_by_email(email):
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Username or email already exists."
        })

    profile_pic_path = save_profile_picture(profile_pic)

    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": hash_password(password),
        "address_line1": address_line1,
        "city": city,
        "state": state,
        "pincode": pincode,
        "user_type": user_type,
        "profile_pic": profile_pic_path
    }

    add_user(user_data)
    return RedirectResponse(url="/login", status_code=302)

@router.get("/login", response_class=HTMLResponse)
def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials."
        })

    # Redirect to dashboard based on user type
    if user["user_type"].lower() == "patient":
        return RedirectResponse(url=f"/dashboard/patient/{username}", status_code=302)
    else:
        return RedirectResponse(url=f"/dashboard/doctor/{username}", status_code=302)
