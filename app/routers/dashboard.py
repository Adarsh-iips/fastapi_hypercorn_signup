from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import find_user_by_username

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard/patient/{username}", response_class=HTMLResponse)
def patient_dashboard(request: Request, username: str):
    user = find_user_by_username(username)
    if not user:
        return HTMLResponse("User not found", status_code=404)
    return templates.TemplateResponse("patient_dashboard.html", {"request": request, "user": user})

@router.get("/dashboard/doctor/{username}", response_class=HTMLResponse)
def doctor_dashboard(request: Request, username: str):
    user = find_user_by_username(username)
    if not user:
        return HTMLResponse("User not found", status_code=404)
    return templates.TemplateResponse("doctor_dashboard.html", {"request": request, "user": user})
