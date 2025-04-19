import os
import subprocess
from pathlib import Path

from git import Git, InvalidGitRepositoryError, Repo
from security import safe_command


class GitHubCLI:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def run(self, *args):
        cmd = ["gh", *args]
        if self.verbose:
            print(f"⚙️  Running: {' '.join(cmd)}")
        result = safe_command.run(subprocess.run, cmd, check=True, capture_output=not self.verbose, text=True)
        return result.stdout.strip() if not self.verbose else None

    def create_repo(self, name, private=False, description=None):
        args = ["repo", "create", name]
        args += ["--private"] if private else ["--public"]
        if description:
            args += ["--description", description]
        args += ["--confirm"]
        return self.run(*args)

    def list_repos(self):
        return self.run("repo", "list")

    def clone_repo(self, name):
        return self.run("repo", "clone", name)

    @staticmethod
    def version():
        git_version = safe_command.run(subprocess.run, ["git", "--version"], capture_output=True, text=True)
        return git_version


def create_repo(name, private=False, description=None):
    return GitHubCLI().create_repo(name, private, description)


def is_git_repo(path):
    """Check if path is a valid Git repository"""
    try:
        # Check if .git exists or path is a valid repo
        return os.path.exists(os.path.join(path, ".git")) or bool(Repo(path).git_dir)
    except InvalidGitRepositoryError:
        return False
    except Exception:  # Catch other potential errors
        return False


def path2repo(dst_path: Path, context: dict[str, str], branch="main"):
    if is_git_repo(dst_path):
        initial = False
        repo = Repo(dst_path)
    else:
        initial = True
        git = Git(dst_path)
        git.init(initial_branch=f"{branch}")
        # Wrap with Repo object
        repo = Repo(dst_path)

    repo.git.checkout(branch)
    repo.git.add(all=True)

    if initial:
        repo.git.commit("-m", "Initial commit by qcradle")
        create_repo(
            name=f"{context['username']}/{context['project_name']}",
            private=context["status"],
            description=context["description"],
        )
        # if "origin" not in [r.name for r in repo.remotes]:
        repo.create_remote("origin", context["ssh_uri"])

    else:
        repo.git.commit("-m", "Update by qcradle")

    # Push to origin main
    repo.remotes.origin.push(refspec=f"{branch}:{branch}")

    # repo.git.add(all=True)
    # repo.git.commit("-m", "Initial commit by qcradle")

    # create_repo(name=f"{context['username']}/{context['project_name']}",
    #            private=context["status"],
    #            description=context["description"])

    # if "origin" not in [r.name for r in repo.remotes]:
    #    repo.create_remote("origin", context['ssh_uri'])

    # Push to origin main
    repo.remotes.origin.push(refspec=f"{branch}:{branch}")
