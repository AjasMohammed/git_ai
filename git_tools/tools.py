from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from .exeptions import NoStagedChangeFound


class GitTools:
    def is_git_repo(self, path: str) -> Repo | None:
        try:
            return Repo(path)
        except NoSuchPathError:
            print(f"The path '{path}' does not exist.")
        except InvalidGitRepositoryError:
            print(f"The path '{path}' is not a valid Git repository.")
        return None

    def get_staged_diff(self, repository: Repo) -> str:
        staged_diff = repository.git.diff("--staged")
        if not staged_diff:
            print(
                f"There are no staged changes in the repository: {self.repository}.")
            raise NoStagedChangeFound
        return staged_diff

    def commit_changes(self, repo: Repo, commit_message: str) -> None:
        try:
            repo.index.commit(commit_message)
        except Exception as e:
            print(f"Error committing changes: {e}")
