"""Git version checking utility using GitPython.

This module provides functionality to check and validate Git version requirements
using the GitPython package, with support for vendor-specific version formats.
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple, Union

from .gh_client import GitHubCLI


class GitVersionError(Exception):
    """Raised when there are issues with Git version requirements."""


class GitNotFoundError(GitVersionError):
    """Raised when Git is not installed or not accessible."""


@dataclass(frozen=True)
class _GitVersion:
    """Represents a semantic Git version.

    This immutable dataclass encapsulates a semantic version number (major.minor.patch)
    with optional vendor-specific information. It provides comparison functionality
    to determine if one version is greater than or equal to another.

    Attributes:
        major (int): The major version number
        minor (int): The minor version number
        patch (Optional[int]): The patch version number, can be None
        vendor_info (Optional[str]): Vendor-specific version information, can be None
    """

    major: int
    minor: int
    patch: Optional[int] = None
    vendor_info: Optional[str] = None

    def __ge__(self, other):
        """Compare if this version is greater than or equal to another version.

        Args:
            other (_GitVersion): Another GitVersion object to compare with

        Returns:
            bool: True if this version is greater than or equal to the other version

        Raises:
            TypeError: If other is not a _GitVersion object
        """
        if not isinstance(other, _GitVersion):
            raise TypeError(f"Cannot compare _GitVersion with {type(other)}")

        # Compare as tuples for a clean lexicographical comparison
        # This handles the case where patch might be None
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

    Returns:
        bool: True if the installed version meets requirements.

    Raises:
        GitVersionError: For version parsing or comparison issues.
        GitNotFoundError: If Git is not installed.
    """
    # --- Convert input to standardized _GitVersion object ---
    # Handle string format (e.g., "2.28.0")
    if isinstance(min_version, str):
        parts = min_version.split(".")
        # Convert parts to integers, with patch being optional
        min_version = _GitVersion(
            int(parts[0]),  # major
            int(parts[1]),  # minor
            int(parts[2]) if len(parts) > 2 else None,  # patch (optional)
        )
    # Handle tuple format (e.g., (2, 28, 0) or (2, 28))
    elif isinstance(min_version, tuple):
        min_version = _GitVersion(
            min_version[0],  # major
            min_version[1],  # minor
            min_version[2] if len(min_version) > 2 else None,  # patch (optional)
        )
    # Note: If min_version is already a _GitVersion object, no conversion needed

    # --- Get installed Git version ---
    # Use GitHubCLI.version() to run the git --version command
    result = GitHubCLI.version()

    # --- Parse the version string ---
    # Check if the command was successful
    if result.returncode == 0:
        # The version string is typically in format: "git version 2.34.1"
        version_str = result.stdout.strip()  # Remove any extra whitespace

        # Use regex to extract just the version numbers
        match = re.match(r"git version (\d+\.\d+\.\d+)", version_str)
        if match:
            # Split the version string into components
            installed_version = match.group(1).split(".")
        else:
            # If we can't parse the version string, it might be in a non-standard format
            raise GitVersionError("Could not parse Git version")
    else:
        # If the command failed, Git is likely not installed
        raise GitNotFoundError("Git is not installed or is not available in the PATH")

    # Create a _GitVersion object from the installed version components
    installed_version = _GitVersion(
        major=int(installed_version[0]),
        minor=int(installed_version[1]),
        patch=int(installed_version[2]),
    )

    # Compare the installed version with the minimum required version
    # The __ge__ method of _GitVersion handles the comparison logic
    return installed_version >= min_version


def assert_git_version(min_version: Union[str, Tuple[int, int], Tuple[int, int, int]]) -> None:
    """Assert that Git version meets minimum requirements.

    Args:
        min_version: Minimum required version (same format as check_git_version).

    Raises:
        GitVersionError: If version requirements are not met.
        GitNotFoundError: If Git is not installed.
    """
    if not _check_git_version(min_version):
        raise GitVersionError(f"Insufficient Git version (required: >= {min_version})")
