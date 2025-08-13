from config import templates
from fastapi import Depends, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from git_tools.exeptions import NoStagedChangeFound
from database import get_db
from models import Repository
from sqlalchemy.orm import Session
from git_tools.tools import GitTools
# from worksheet_tools.sheets import Sheets

router = APIRouter()


@router.post("/add-repo", name="add_repo", response_class=HTMLResponse)
def add_repo(request: Request, repo_path: str = Form(...), repo_name: str = Form(...), db: Session = Depends(get_db)) -> HTMLResponse:
    """
    Add a repository to the application.
    """
    print(f"Adding repo: {repo_name} at {repo_path}")
    tools = GitTools()
    if tools.init_repo(repo_path):
        repo = Repository(name=repo_name, url=repo_path)
        db.add(repo)
        db.commit()
    else:
        print("Invalid repo path")
    repos = db.query(Repository).all()
    return templates.TemplateResponse("partials/git/repo_list.html", {"request": request, 'repos': repos})


@router.post("/generate-commit-message", name="generate_commit_message", response_class=HTMLResponse)
def generate_commit_message(request: Request, repo_id: str = Form(...), additional_instruction: str = Form(...), db: Session = Depends(get_db)) -> HTMLResponse:
    """
    Generate a commit message for the repository.
    """
    repo: Repository | None = db.get(Repository, repo_id)
    print(f"Generating commit message for repo: {repo.name}")
    if repo:
        try:
            # llm = GitAI(repo, api_key=llm_api_key)
            # print("Invoking LLM")
            # commit_message = llm.invoke(
            #     task='commit-message', additional_instruction=additional_instruction)
            # print(f"Generated commit message: {commit_message}")
            commit_message = "This is a placeholder commit message."
        except NoStagedChangeFound:
            commit_message = "There are no staged changes in the specified repository."
        except Exception as e:
            print(f"Error generating commit message: {e}")
            commit_message = e
    else:
        commit_message = None
    return templates.TemplateResponse("partials/git/commit_message.html", {"request": request, 'commit_message': commit_message, 'repo_id': repo_id, 'commit': True})


@router.post("/commit-changes", name="commit_changes", response_class=HTMLResponse)
def commit_changes(request: Request, repo_id: str = Form(...), commit_message: str = Form(...), db: Session = Depends(get_db)) -> HTMLResponse:
    """
    Commit changes in the repository.
    """
    repo: Repository | None = db.get(Repository, repo_id)
    git_tools = GitTools()
    print(
        f"Committing changes for repo: {repo.name} with message: {commit_message}")
    if repo:
        try:
            git_repo = git_tools.init_repo(repo.url)
            if git_repo:
                git_tools.commit_changes(git_repo, commit_message)
        except Exception as e:
            print(f"Error initializing repository: {e}")
            return templates.TemplateResponse("partials/git/commit_message.html", {"request": request, 'commit': True, "commit_message": commit_message, 'repo_id': repo_id})

    return templates.TemplateResponse("partials/git/commit_message.html", {"request": request, 'commit': False})


@router.post("/remove-repo/{repo_id}", name="remove_repo", response_class=HTMLResponse)
def remove_repo(request: Request, repo_id: str, db: Session = Depends(get_db)):
    print(f"Removing repo: {repo_id}")
    repo: Repository | None = db.get(Repository, repo_id)
    if repo:
        db.delete(repo)
        db.commit()
    return templates.TemplateResponse("partials/git/repo_list.html", {"request": request, 'repos': db.query(Repository).all()})
