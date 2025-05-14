"""GitHub CLI integration module for repository management.

This module provides classes and functions for interacting with GitHub
through the GitHub CLI (gh) and Git commands. It includes functionality
for creating repositories, checking repository status, and setting up
Git repositories with GitHub integration.
"""

import subprocess
from pathlib import Path
from typing import Dict, Optional

from git import Git, InvalidGitRepositoryError, Repo
from security import safe_command


class GitHubCLI:
    """A wrapper class for GitHub CLI commands.

    This class provides methods to interact with GitHub through the GitHub CLI (gh)
    command-line tool. It handles command execution, error handling, and provides
    convenience methods for common GitHub operations.

    Attributes:
        verbose (bool): Whether to print command execution details to stdout.
    """

    def __init__(self, verbose: bool = True):
        """Initialize a new GitHubCLI instance.

        Args:
            verbose (bool, optional): Whether to print command execution details.
                Defaults to True.
        """
        self.verbose = verbose

    def run(self, *args: str) -> Optional[str]:
        """Execute a GitHub CLI command safely.

        This method runs a GitHub CLI command with the provided arguments,
        handles errors, and returns the command output if successful.

        Args:
            *args: Variable length argument list of strings to pass to the GitHub CLI.

        Returns:
            Optional[str]: The command output if verbose is False, None otherwise.

        Raises:
            RuntimeError: If the GitHub CLI command fails.
        """
        # Construct the command by prepending 'gh' to the arguments
        cmd = ["gh", *args]
        if self.verbose:
            print(f"⚙️  Running: {' '.join(cmd)}")

        try:
            # Use safe_command.run to execute the command securely
            # - check=True ensures that CalledProcessError is raised for non-zero exit codes
            # - capture_output controls whether stdout/stderr are captured or displayed
            # - text=True ensures output is returned as strings, not bytes
            result = safe_command.run(subprocess.run, cmd, check=True, capture_output=not self.verbose, text=True)

            # Only return stdout if we're not in verbose mode (otherwise it's already printed)
            return result.stdout.strip() if not self.verbose else None
        except subprocess.CalledProcessError as e:
            # Log the error if in verbose mode
            if self.verbose:
                print(f"❌ Command failed: {e.stderr}")
            # Re-raise as a RuntimeError with more context
            raise RuntimeError(f"GitHub CLI error: {e.stderr}") from e

    def create_repo(self, name: str, private: bool = False, description: Optional[str] = None) -> str:
        """Create a new GitHub repository.

        Args:
            name (str): The name of the repository to create.
                Spaces will be replaced with hyphens.
            private (bool, optional): Whether the repository should be private.
                Defaults to False (public).
            description (Optional[str], optional): A description for the repository.
                Defaults to None.

        Returns:
            str: The output from the GitHub CLI command.

        Raises:
            RuntimeError: If the repository creation fails.
        """
        args = ["repo", "create", name.replace(" ", "-")]
        args += ["--private"] if private else ["--public"]
        if description:
            args += ["--description", description]
        args += ["--confirm"]
        return self.run(*args)

    @staticmethod
    def version() -> str:
        """Verify GitHub CLI is installed and return Git version.

        Returns:
            str: The Git version string.

        Raises:
            subprocess.CalledProcessError: If Git is not installed or the command fails.
        """
        try:
            return safe_command.run(subprocess.run, ["git", "--version"], capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise subprocess.CalledProcessError("Git is not installed")


def is_git_repo(path: Path) -> bool:
    """Check if path contains a valid Git repository.

    This function checks if the given path contains a valid Git repository
    by looking for a .git directory or using GitPython's Repo class.

    Args:
        path (Path): The path to check for a Git repository.

    Returns:
        bool: True if the path contains a valid Git repository, False otherwise.
    """
    try:
        # First, try a simple check for a .git directory (faster)
        git_dir = path / ".git"

        # If .git directory exists, it's a Git repo
        # If not, try using GitPython's Repo class which can detect
        # Git repositories with non-standard structures
        return git_dir.exists() or bool(Repo(str(path)).git_dir)
    except InvalidGitRepositoryError:
        # GitPython throws this when the path is not a Git repository
        return False
    except Exception as e:
        # Catch any other exceptions (file access issues, etc.)
        print(f"⚠️  Error checking Git repo: {e}")
        return False


def setup_repository(dst_path: Path, context: Dict[str, str], branch: str = "main") -> Repo:
    """Initialize or update a Git repository with GitHub integration.

    This function sets up a Git repository at the specified path, initializing
    a new one if it doesn't exist or updating an existing one. It also handles
    GitHub integration, creating a remote repository if needed and pushing changes.

    Args:
        dst_path (Path): The path where the repository should be set up.
        context (Dict[str, str]): A dictionary containing project information,
            including 'username', 'project_name', 'ssh_uri', 'status' (optional),
            and 'description' (optional).
        branch (str, optional): The branch to use. Defaults to "main".

    Returns:
        Repo: The GitPython Repo object for the repository.

    Raises:
        RuntimeError: If GitHub CLI is not installed.
    """
    # Verify GitHub CLI is installed before proceeding
    if not GitHubCLI.version():
        raise RuntimeError("GitHub is not installed")

    # Ensure dst_path is a Path object for consistent handling
    dst_path = Path(dst_path)

    # --- Repository initialization phase ---
    # Check if the destination already contains a Git repository
    if is_git_repo(dst_path):
        # For existing repositories, open and switch to the specified branch
        repo = Repo(str(dst_path))
        repo.git.checkout(branch)
        initial = False  # Flag to track that this is an update, not a new repo
    else:
        # For new repositories, initialize with the specified branch
        # Using initial_branch ensures Git uses the right branch name from the start
        Git(str(dst_path)).init(initial_branch=branch)
        repo = Repo(str(dst_path))
        initial = True  # Flag to track that this is a new repository

    # --- Changes management phase ---
    # Stage all changes in the repository (new files, modifications, deletions)
    repo.git.add(A=True)

    # Commit the changes with an appropriate message based on whether this is initial setup or an update
    commit_message = "Initial commit by qcradle" if initial else "Update by qcradle"
    repo.git.commit(m=commit_message)

    # --- GitHub integration phase ---
    # Only create a new GitHub repository if this is the initial setup
    if initial:
        gh = GitHubCLI()
        # Create the GitHub repository using the project information from context
        gh.create_repo(
            name=f"{context['username']}/{context['project_name']}",
            private=context.get("status", False),  # Default to public if status not provided
            description=context.get("description", ""),  # Default to empty description if not provided
        )

        # Add the remote if it doesn't already exist
        # This connects the local repository to the GitHub repository
        if not any(r.name == "origin" for r in repo.remotes):
            repo.create_remote("origin", context["ssh_uri"])

    # --- Push changes to GitHub ---
    # Push the changes to the remote repository, ensuring the branch exists remotely
    # The refspec format "branch:branch" ensures the local branch is pushed to the same-named remote branch
    repo.remotes.origin.push(refspec=f"{branch}:{branch}")

    return repo
