from git import Repo
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from .tools import GitTools


class GitAI:
    def __init__(
            self,
            repo_path,
            model: str = "gemini-2.0-flash",
            model_provider: str = "google_genai",
            api_key: str | None = None,
            tools = GitTools()
    ):
        self.repository: Repo = tools.is_git_repo(repo_path)
        self.llm = init_chat_model(
            model,
            model_provider=model_provider,
            api_key=api_key
        )
        self.tools = tools


    def get_initial_prompt(self, task='commit-message') -> list:
        if task == 'commit-message':
            return [SystemMessage(content="""
            You are a helpful AI assistant specialized in analyzing code diffs and generating clear, descriptive, and concise commit messages. Your task is to take input in the form of code diffs (unified format) and generate an ideal commit message following conventional commit standards.

            Guidelines:
            - Summarize what the diff achieves, not how it does it.
            - Use a conventional commit prefix like `feat`, `fix`, `refactor`, `docs`, `test`, or `chore` to seperate the commit messages according to the changes for readability.
            - The message should be in past tense (e.g., "added", "modified", "initialized", etc).
            - Be concise but descriptive and detailed enough to understand the purpose of the change.
            - Do not include file names or file paths unless essential.
            - Prefer past tense imperative mood (e.g., “added support for...”, “fixed issue where...”, “refactored redundant logic”).
            - include backticks(``) to highlight the main parts the points should be started with a dash(-).

            Example Input:
            ```diff
            - if user.is_authenticated:
            -     return redirect('dashboard')
            + if not user.is_authenticated:
            +     return redirect('login')
            ```

            Expected Output:
            fix: redirect unauthenticated users to login page instead of dashboard
            - added conditional statements to check if the user is authenticated.
            - if authenticated, the user is redirected to the dashboard.
            - if not authenticated, the user is redirected to the login page
            """)]
        return

    def invoke(self, task: str) -> BaseMessage:
        if task == 'commit-message':
            staged_changes = self.tools.get_staged_diff(self.repository)
            prompt_message = self.get_initial_prompt()
            prompt_message.append(HumanMessage(content=staged_changes))
            response = self.llm.invoke(prompt_message).content
            return response
