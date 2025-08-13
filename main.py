from fastapi import FastAPI
from database import engine, Base
# from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from utils import load_repos
from config import in_container, base_path, database_url
from routers import git_end, home

print("Container: ", in_container)
print("Database URL: ", database_url)

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



app.include_router(home.router)
app.include_router(git_end.router, prefix="/git", tags=["git"])