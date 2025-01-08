#    Copyright 2023 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Git version checking utility using GitPython.

This module provides functionality to check and validate Git version requirements
using the GitPython package, with support for vendor-specific version formats.
"""

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

from git import Git, GitCommandError, GitCommandNotFound, InvalidGitRepositoryError, NoSuchPathError, Repo


class GitVersionError(Exception):
    """Raised when there are issues with Git version requirements."""


class GitNotFoundError(GitVersionError):
    """Raised when Git is not installed or not accessible."""


@dataclass
class GitVersion:
    """Represents a semantic Git version."""

    major: int
    minor: int
    patch: Optional[int] = None
    vendor_info: Optional[str] = None

    def __str__(self) -> str:
        """Convert version to string representation."""
        version = f"{self.major}.{self.minor}"
        if self.patch is not None:
            version = f"{version}.{self.patch}"
        if self.vendor_info:
            version = f"{version} ({self.vendor_info})"
        return version

    def meets_minimum(self, min_version: "GitVersion") -> bool:
        """Check if this version meets the minimum required version."""
        if self.major != min_version.major:
            return self.major > min_version.major
        if self.minor != min_version.minor:
            return self.minor > min_version.minor
        if self.patch is not None and min_version.patch is not None:
            return self.patch >= min_version.patch
        return True


def get_git_version() -> str:
    """Get the installed Git version string using GitPython.

    Returns:
        str: Raw version string from Git.

    Raises:
        GitNotFoundError: If Git is not installed or accessible.
        GitVersionError: If the Git version command fails.
    """
    try:
        git = Git()
        return git.version()
    except GitCommandNotFound:
        raise GitNotFoundError("Git is not installed or not found in PATH")
    except GitCommandError as e:
        raise GitVersionError(f"Git version check failed: {e.stderr.strip()}")


def parse_version(version_str: str) -> GitVersion:
    """Parse a Git version string into a GitVersion object.

    Handles various Git version formats including vendor-specific versions:
    - Standard: "git version 2.39.5"
    - Apple: "git version 2.39.5 (Apple Git-154)"
    - Other vendor versions with additional information

    Args:
        version_str: Raw version string from Git.

    Returns:
        GitVersion: Parsed version information.

    Raises:
        GitVersionError: If the version string cannot be parsed.
    """
    # Match version pattern with optional vendor info
    pattern = r"git version (\d+)\.(\d+)\.(\d+)(?:\s+\((.*?)\))?"
    match = re.match(pattern, version_str)

    if not match:
        # Try alternative pattern without patch version
        pattern = r"git version (\d+)\.(\d+)(?:\s+\((.*?)\))?"
        match = re.match(pattern, version_str)

    if not match:
        raise GitVersionError(f"Unable to parse Git version from: {version_str}")

    try:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3)) if len(match.groups()) > 2 and match.group(3) else None
        vendor_info = match.group(4) if len(match.groups()) > 3 else None

        return GitVersion(major=major, minor=minor, patch=patch, vendor_info=vendor_info)
    except (IndexError, ValueError) as e:
        raise GitVersionError(f"Error parsing version components from: {version_str}") from e


def check_git_version(
    min_version: Union[str, GitVersion, Tuple[int, int], Tuple[int, int, int]],
    verbose: bool = False,
    repo_path: Optional[str] = None,
) -> bool:
    """Check if the installed Git version meets minimum requirements.

    Args:
        min_version: Minimum required version, specified as either:
            - A string (e.g., "2.28.0" or "2.28")
            - A GitVersion object
            - A tuple of (major, minor) or (major, minor, patch)
        verbose: If True, print version information.
        repo_path: Optional path to Git repository to check.

    Returns:
        bool: True if the installed version meets requirements.

    Raises:
        GitVersionError: For version parsing or comparison issues.
        GitNotFoundError: If Git is not installed.
    """
    # Convert min_version to GitVersion object
    if isinstance(min_version, str):
        parts = min_version.split(".")
        min_version = GitVersion(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else None)
    elif isinstance(min_version, tuple):
        min_version = GitVersion(min_version[0], min_version[1], min_version[2] if len(min_version) > 2 else None)

    try:
        # Get and parse installed version
        git = Git(repo_path) if repo_path else Git()
        version_str = git.execute(["git", "--version"])
        installed_version = parse_version(version_str)

        if verbose:
            print(f"Installed Git version: {installed_version}")
            print(f"Minimum required version: {min_version}")
            if repo_path:
                print(f"Repository path: {repo_path}")

        return installed_version.meets_minimum(min_version)

    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        raise GitVersionError(f"Invalid repository path: {repo_path}") from e


def assert_git_version(
    min_version: Union[str, GitVersion, Tuple[int, int], Tuple[int, int, int]], repo_path: Optional[str] = None
):
    """Assert that Git version meets minimum requirements.

    Args:
        min_version: Minimum required version (same format as check_git_version).
        repo_path: Optional path to Git repository to check.

    Raises:
        GitVersionError: If version requirements are not met.
        GitNotFoundError: If Git is not installed.
    """
    if not check_git_version(min_version, repo_path=repo_path):
        git = Git(repo_path) if repo_path else Git()
        version_str = git.execute(["git", "--version"])
        installed_version = parse_version(version_str)
        if isinstance(min_version, (str, tuple)):
            min_version = (
                parse_version(f"git version {min_version}")
                if isinstance(min_version, str)
                else GitVersion(*min_version)
            )
        raise GitVersionError(f"Insufficient Git version: {installed_version} " f"(required: >= {min_version})")


def get_git_info(repo_path: Optional[str] = None) -> dict:
    """Get comprehensive Git information.

    Args:
        repo_path: Optional path to Git repository.

    Returns:
        dict: Dictionary containing Git information including:
            - version: Installed Git version (GitVersion object)
            - exec_path: Path to Git executable
            - python_git: GitPython version
            - vendor_info: Vendor-specific information (if any)

    Raises:
        GitVersionError: If Git information cannot be retrieved.
    """
    try:
        git = Git(repo_path) if repo_path else Git()
        version_str = git.execute(["git", "--version"])
        version = parse_version(version_str)

        return {
            "version": version,
            "exec_path": git.git_exec_name,
            "python_git": git.GIT_PYTHON_VERSION,
            "repo_path": repo_path if repo_path else "Not specified",
            "vendor_info": version.vendor_info,
        }
    except Exception as e:
        raise GitVersionError(f"Failed to retrieve Git information: {str(e)}")


def init_git_repo(path: Path, ssh_uri: str, logger=None):
    logger = logger or logging.getLogger(__name__)
    """Initialize a Git repository using GitPython and push to remote"""
    try:
        # Initialize Git repository
        repo = Repo.init(path)
        logger.info(f"Git repository initialized at {path}")

        # add all files
        repo.git.add(".")
        repo.index.commit("Initial commit")

        repo.create_remote("origin", ssh_uri)
        # Add the remote origin
        origin = repo.create_remote("origin", ssh_uri)
        logger.info(f"Remote origin set to {ssh_uri}")

        # Add all files
        repo.git.add(A=True)
        logger.info("Staged all files.")

        # Commit the changes
        repo.index.commit("Initial commit")
        logger.info("Committed the changes.")

        # Push the changes to remote
        origin.push(refspec="main:main")
        logger.info("Pushed to remote repository.")

    except GitCommandError as e:
        logger.error(f"Git command failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize or push the Git repository: {e}")
        return False

    return True
