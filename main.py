from fastapi import Depends, FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from git_tools.exeptions import NoStagedChangeFound
from database import engine, Base, SessionLocal
# from contextlib import asynccontextmanager
from models import Repository
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from decouple import config
from git_tools.git_ai import GitAI
from git_tools.tools import GitTools
from utils import load_repos


llm_api_key: str = config("LLM_API_KEY", default="")
in_container: str = config("IN_CONTAINER", default="", cast=bool)
base_path: str = config("BASE_REPOS_PATH", default="/repos")

print("Container: ", in_container)


def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    """
    Base.metadata.create_all(bind=engine)
    if in_container:
        print("=============================")
        print("Running in container")
        print("=============================")
        print("Loading paths from container")
        load_repos(base_path)
    yield
    # Cleanup code can be added here if needed.


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="templates/static"), name="static")
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """
    Home page of the application.
    """
    repos = db.query(Repository).all()
    model_provider = "google_genai"
    model = "gemini-2.0-flash"
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request, "name": "Ajas",
            "title": "Home | FastAPI App",
            "year": datetime.now().year,
            "repos": repos,
            "model_provider": model_provider,
            "model": model
        }
    )


@app.post("/add-repo", response_class=HTMLResponse)
def add_repo(request: Request, repo_path: str = Form(...), repo_name: str = Form(...), db: Session = Depends(get_db)) -> HTMLResponse:
    """
    Add a repository to the application.
    """
    print(f"Adding repo: {repo_name} at {repo_path}")
    tools = GitTools()
    if tools.is_git_repo(repo_path):
        repo = Repository(name=repo_name, url=repo_path)
        db.add(repo)
        db.commit()
    else:
        print("Invalid repo path")
    repos = db.query(Repository).all()
    return templates.TemplateResponse("partials/repo_list.html", {"request": request, 'repos': repos})


@app.post("/generate-commit-message", response_class=HTMLResponse)
def generate_commit_message(request: Request, repo_id: str = Form(...), db: Session = Depends(get_db)) -> HTMLResponse:
    """
    Generate a commit message for the repository.
    """
    repo: Repository | None = db.get(Repository, repo_id)
    print(f"Generating commit message for repo: {repo.name}")
    if repo:
        try:
            llm = GitAI(repo, api_key=llm_api_key)
            print("Invoking LLM")
            commit_message = llm.invoke(task='commit-message')
        except NoStagedChangeFound:
            commit_message = "There are no staged changes in the specified repository."
        except Exception as e:
            print(f"Error generating commit message: {e}")
            commit_message = e
    else:
        commit_message = None
    return templates.TemplateResponse("partials/commit_message.html", {"request": request, 'commit_message': commit_message})
