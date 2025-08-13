from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from datetime import datetime
from models import Repository
from sqlalchemy.orm import Session
from database import get_db
from config import templates

# Define the router for the home page
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request, tab: str = "git", db: Session = Depends(get_db),) -> HTMLResponse:
    """
    Home page of the application.
    """
    print(f"Loading home page with tab: {tab}")
    repos = db.query(Repository).all()
    model_provider = "google_genai"
    model = "gemini-2.0-flash"
    page_template = "home.html"
    if tab == "task":
        page_template = "task.html"
    return templates.TemplateResponse(
        page_template,
        {
            "request": request,
            "name": "Ajas",
            "title": "Home | FastAPI App",
            "year": datetime.now().year,
            "repos": repos,
            "model_provider": model_provider,
            "model": model
        }
    )
