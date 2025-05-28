import subprocess
from pathlib import Path
from typing import Dict, Optional

from git import Git, InvalidGitRepositoryError, Repo
from security import safe_command


class GitHubCLI:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def run(self, *args: str) -> Optional[str]:
        """Execute a GitHub CLI command safely."""
        cmd = ["gh", *args]
        if self.verbose:
            print(f"⚙️  Running: {' '.join(cmd)}")

        try:
            result = safe_command.run(subprocess.run, cmd, check=True, capture_output=not self.verbose, text=True)
            return result.stdout.strip() if not self.verbose else None
        except subprocess.CalledProcessError as e:
            if self.verbose:
                print(f"❌ Command failed: {e.stderr}")
            raise RuntimeError(f"GitHub CLI error: {e.stderr}") from e

    def create_repo(self, name: str, private: bool = False, description: Optional[str] = None) -> str:
        """Create a new GitHub repository."""
        args = ["repo", "create", name.replace(" ", "-")]
        args += ["--private"] if private else ["--public"]
        if description:
            args += ["--description", description]
        args += ["--confirm"]
        return self.run(*args)

    @staticmethod
    def version() -> str:
        """Verify GitHub CLI is installed."""
        try:
            return safe_command.run(subprocess.run, ["git", "--version"], capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise subprocess.CalledProcessError("Git is not installed")


def is_git_repo(path: Path) -> bool:
    """Check if path contains a valid Git repository using pathlib only."""
    try:
        git_dir = path / ".git"
        return git_dir.exists() or bool(Repo(str(path)).git_dir)
    except InvalidGitRepositoryError:
        return False
    except Exception as e:
        print(f"⚠️  Error checking Git repo: {e}")
        return False


def setup_repository(dst_path: Path, context: Dict[str, str], branch: str = "main") -> Repo:
    """Initialize or update a Git repository with GitHub integration."""
    if not GitHubCLI.version():
        raise RuntimeError("GitHub is not installed")

    # Convert to Path if not already
    dst_path = Path(dst_path)

    # Initialize or open repository
    if is_git_repo(dst_path):
        repo = Repo(str(dst_path))
        repo.git.checkout(branch)
        initial = False
    else:
        Git(str(dst_path)).init(initial_branch=branch)
        repo = Repo(str(dst_path))
        initial = True
        print("initial")

    # Stage all changes
    repo.git.add(A=True)

    # Commit changes
    commit_message = "Initial commit by qcradle" if initial else "Update by qcradle"
    repo.git.commit(m=commit_message)

    # Create remote repository if initial setup
    if initial:
        gh = GitHubCLI()
        if context["status"] == "public":
            private = False
        else:
            private = True

        gh.create_repo(
            name=f"{context['username']}/{context['project_name']}",
            private=private,
            description=context.get("description", ""),
        )

        # Add remote if it doesn't exist
        if not any(r.name == "origin" for r in repo.remotes):
            repo.create_remote("origin", context["ssh_uri"])

    # Push changes
    repo.remotes.origin.push(refspec=f"{branch}:{branch}")

    return repo
