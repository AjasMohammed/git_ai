import os
from git_tools.tools import GitTools
from models import Repository
from database import SessionLocal


def filter_repo_directories(paths: list, base_path: str) -> dict:
    repos = {}
    tools = GitTools()
    for path in paths:
        full_path = os.path.join(base_path, path)
        dir_name = os.path.basename(full_path).replace("_", " ").title()
        if os.path.isdir(full_path) and tools.is_git_repo(full_path):
            repos[dir_name] = full_path
        else:
            print(f"Skipping {full_path} as it is not a Git repository.")
    return repos


def load_repos(base_path: str) -> None:
    """
    Load repositories from a directory and add them to the database.
    Note:
        This function will be called when the application starts on a container.
        The BASE_REPOS_PATH variable is defined in the .env file.
    """
    dirs = os.listdir(base_path)
    try:
        db = SessionLocal()
        repos = filter_repo_directories(dirs, base_path)
        for repo_name, repo_path in repos.items():
            exists = db.query(Repository).filter_by(url=repo_path).first()
            if not exists:
                repo = Repository(name=repo_name, url=repo_path)
                db.add(repo)
                db.commit()
                print(f"Added repo: {repo_name} at {repo_path}")
            else:
                print(f"Repo already exists: {repo_name} at {repo_path}")
    finally:
        db.close()
