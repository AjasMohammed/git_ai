from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from decouple import config
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from google.cloud import firestore
from google.oauth2 import service_account
from langchain_google_firestore import FirestoreChatMessageHistory
from git import Repo
import json

repos = json.load(open("repos.json", "r"))

google_api = config("GOOGLE_API_KEY")
project_id = config('FIREBASE_PROJECT_ID')
session_id = "google_gemini"
collection_name = "commit_messages-v2.2"
firebase_credentials = config('FIREBASE_SERVICE_ACCOUNT')


def init_firestore():
    creads = service_account.Credentials.from_service_account_file(
        firebase_credentials)
    chat_db = firestore.Client(credentials=creads, project=project_id)
    return chat_db


def llm_commit_message(diff, chat_db=None):
    # llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=google_api)
    llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai", api_key=google_api)
    if chat_db:
        chat_history = FirestoreChatMessageHistory(
            session_id=session_id,
            collection=collection_name,
            client=chat_db
        )
    prompt_message = [SystemMessage(content="""
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
    # commit_history = []
    # chat_history.add_message(system_message)

    # with open('ch.txt') as f:
    #     content = f.read()

    # chat_history.add_user_message(diff)
    prompt_message.append(HumanMessage(content=diff))
    result = llm.invoke(prompt_message)
    response = result.content
    # chat_history.add_ai_message(response)
    prompt_message.append(AIMessage(content=response))
    # print(response)
    return response


try:
    git_repo = input('Enter the path to your Git Repo: ')
    git_repo_path = repos[git_repo]
    repo = Repo(git_repo_path)
    staged_diff = repo.git.diff('--staged')

    if staged_diff:
        # fire_store = init_firestore()
        print("Inintialized Firestore!")
        print("Connecting LLM!")
        response = llm_commit_message(staged_diff)
        print("Generated commit message!")
        while True:
            commit_permission = input(
                "1) Commit the changes along with the commit message automatically.\n2) Output the commit message in the terminal.\n>>> ")
            if int(commit_permission) == 1:
                repo.index.commit(response)
                break
            elif int(commit_permission) == 2:
                print()
                print(response)
                print()
                break
            else:
                print("Invalid input!")
                print()
        with open('CM.txt', "w") as file:
            file.write(response)
        print()
    else:
        print("The staging area is empty! You have to add files to the staging area to generate commit message.")
    # print(chat_history.messages)

except KeyError:
    print("Invalid repo name!")
except Exception as e:
    print(e)
