"""Git version checking utility using GitPython.

This module provides functionality to check and validate Git version requirements
using the GitPython package, with support for vendor-specific version formats.
"""

import re
import subprocess
from dataclasses import dataclass
from typing import Optional, Tuple, Union


class GitVersionError(Exception):
    """Raised when there are issues with Git version requirements."""


class GitNotFoundError(GitVersionError):
    """Raised when Git is not installed or not accessible."""


@dataclass(frozen=True)
class _GitVersion:
    """Represents a semantic Git version."""

    major: int
    minor: int
    patch: Optional[int] = None
    vendor_info: Optional[str] = None

    def __ge__(self, other):
        if not isinstance(other, _GitVersion):
            raise TypeError(f"Cannot compare _GitVersion with {type(other)}")
        # Compare major, minor, and patch numbers
        return (self.major, self.minor, self.patch) >= (
            other.major,
            other.minor,
            other.patch,
        )


def _check_git_version(
    min_version: Union[str, Tuple[int, int], Tuple[int, int, int]],
) -> bool:
    """Check if the installed Git version meets minimum requirements.

    Args:
        min_version: Minimum required version, specified as either:
            - A string (e.g., "2.28.0" or "2.28")
            - A GitVersion object
            - A tuple of (major, minor) or (major, minor, patch)
        verbose: If True, print version information.

    Returns:
        bool: True if the installed version meets requirements.

    Raises:
        GitVersionError: For version parsing or comparison issues.
        GitNotFoundError: If Git is not installed.
    """
    # Convert min_version to GitVersion object
    if isinstance(min_version, str):
        parts = min_version.split(".")
        min_version = _GitVersion(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else None)
    elif isinstance(min_version, tuple):
        min_version = _GitVersion(
            min_version[0],
            min_version[1],
            min_version[2] if len(min_version) > 2 else None,
        )

    # Run the git --version command using subprocess
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        # The version string is like: "git version 2.34.1"
        version_str = result.stdout.strip()  # Remove any extra whitespace
        # Extract the version using a regular expression
        match = re.match(r"git version (\d+\.\d+\.\d+)", version_str)
        if match:
            installed_version = match.group(1).split(".")
        else:
            raise GitVersionError("Could not parse Git version")
    else:
        raise GitNotFoundError("Git is not installed or is not available in the PATH")

    installed_version = _GitVersion(
        major=int(installed_version[0]),
        minor=int(installed_version[1]),
        patch=int(installed_version[2]),
    )

    return installed_version >= min_version


def assert_git_version(min_version: Union[str, Tuple[int, int], Tuple[int, int, int]]):
    """Assert that Git version meets minimum requirements.

    Args:
        min_version: Minimum required version (same format as check_git_version).

    Raises:
        GitVersionError: If version requirements are not met.
        GitNotFoundError: If Git is not installed.
    """
    if not _check_git_version(min_version):
        raise GitVersionError(f"Insufficient Git version (required: >= {min_version})")
