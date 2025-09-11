from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from .exeptions import NoStagedChangeFound


class GitTools:
    def init_repo(self, path: str) -> Repo | None:
        """
        Checks if a given path is a valid Git repository.

        Args:
            path (str): The path to check.

        Returns:
            Repo | None: The Repo object if the path is a valid Git repository, or None if it is not.
        """
        try:
            print(f"Checking if '{path}' is a Git repository...")
            return Repo(path)
        except NoSuchPathError:
            print(f"The path '{path}' does not exist.")
        except InvalidGitRepositoryError:
            print(f"The path '{path}' is not a valid Git repository.")
        return None

    def current_branch(self, repository: Repo | None) -> str:
        """
        Get the current branch of a repository.

        Args:
            repository: A git repository.

        Returns:
            The name of the current branch.

        Raises:
            ValueError: If the repository is None or if it has no branches.
        """
        if not repository or not repository.branches:
            raise ValueError("Repository is None or has no branches.")
        return repository.active_branch.name

    def get_staged_diff(self, repository: Repo | None) -> str:
        """
        Get the staged changes of a repository as a string.

        Args:
            repository: A git repository.

        Returns:
            A string containing the staged changes of the repository.

        Raises:
            NoStagedChangeFound: If there are no staged changes in the repository.
        """
        staged_diff: str | None = repository.git.diff("--cached")
        if not staged_diff:
            print(
                f"There are no staged changes in the repository: {repository}.")
            raise NoStagedChangeFound
        return staged_diff

    def commit_changes(self, repo: Repo, commit_message: str) -> None:
        """
        Commit changes in a repository.

        Args:
            repo (Repo): The repository to commit.
            commit_message (str): The commit message.

        Raises:
            Exception: If there is an error committing the changes.
        """
        try:
            repo.index.commit(commit_message)
            print(f"Changes committed to {repo.branches} with message: {commit_message}")
        except Exception as e:
            print(f"Error committing changes: {e}")

