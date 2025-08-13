from decouple import config
from fastapi.templating import Jinja2Templates


llm_api_key: str = config("LLM_API_KEY", default="")
in_container: str = config("IN_CONTAINER", default="", cast=bool)
base_path: str = config("BASE_REPOS_PATH", default="/repos")
templates = Jinja2Templates(directory="templates")
database_url: str = config("DATABASE_URL", default="sqlite:///repos.db")
