from git import Repo
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from .tools import GitTools
from models import CommitData, Repository
from database import get_db


class GitAI:
    def __init__(
            self,
            repo: Repository,
            model: str = "gemini-2.0-flash",
            model_provider: str = "google_genai",
            api_key: str | None = None,
            tools=GitTools()
    ):
        self.repo_id = repo.id
        self.repository: Repo | None = tools.is_git_repo(repo.url)
        self.llm = init_chat_model(
            model,
            model_provider=model_provider,
            api_key=api_key
        )
        self.tools = tools

    def get_initial_prompt(self, task='commit-message') -> list:
        if task == 'commit-message':
            return [SystemMessage(content="""
                        You are an AI assistant that generates descriptive and conventional commit messages from git diffs.

                        Your task:
                        - Take unified diff as input.
                        - Generate a conventional commit message with a short summary and bullet points.

                        Follow this format:

                        <type>: <summary in past tense>
                        - <point 1 explaining the main change>
                        - <point 2 (if needed)>
                        - <point 3 (if needed)>

                        Conventional commit types include: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`.

                        Instructions:
                        - Summarize what changed, not how.
                        - Use past tense (e.g., “added”, “removed”, “updated”).
                        - Be clear and concise.
                        - Do not mention file names or paths.
                        - Highlight technical terms or code-related phrases using backticks.

                        Example:

                        Input:
                        ```diff
                        - if user.is_authenticated:
                        -     return redirect('dashboard')
                        + if not user.is_authenticated:
                        +     return redirect('login')

                    """)]
        return

    def save_data(self, diff: str, commit_message: str):
        try:
            with get_db() as db:
                commit_data = CommitData(git_diff=diff, commit_message=commit_message, repo_id=self.repo_id)
                db.add(commit_data)
                db.commit()
            return True
        except Exception as e:
            print(f"Error saving commit data: {e}")
            return False

    def invoke(self, task: str) -> BaseMessage | None:
        if task == 'commit-message':
            staged_changes = self.tools.get_staged_diff(self.repository)
            prompt_message = self.get_initial_prompt()
            prompt_message.append(HumanMessage(content=staged_changes))
            response = self.llm.invoke(prompt_message).content
            self.save_data(staged_changes, response)
            return response
