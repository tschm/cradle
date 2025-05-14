"""User input collection and validation module.

This module provides functions for collecting and validating user input
for GitHub repository creation. It includes validation functions for
project names, usernames, descriptions, and repository visibility status.
"""

import logging
import re
from typing import Any, Dict, Optional

import questionary


def _validate_project_name(project_name: str) -> str:
    """Validate and normalize a project name.

    This function checks if the project name follows the required format:
    - Starts with a lowercase letter
    - Contains only lowercase letters, digits, dashes, or underscores
    - Does not start or end with a dash or underscore

    Args:
        project_name (str): The project name to validate.

    Returns:
        str: The validated and stripped project name.

    Raises:
        ValueError: If the project name does not meet the requirements.
    """
    # Remove leading/trailing whitespace
    project_name = project_name.strip()

    # Validate with regular expression:
    # ^[a-z]                 - Start with a lowercase letter
    # [a-z0-9]*              - Followed by zero or more lowercase letters or digits
    # (?:[-_][a-z0-9]+)*$    - Optionally followed by groups that:
    #                           - Start with a dash or underscore
    #                           - Followed by one or more lowercase letters or digits
    #                           - Can repeat zero or more times
    #                           - Must end the string
    # This ensures no consecutive dashes/underscores and none at the end
    if not re.match(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$", project_name):
        raise ValueError(
            "Project name must start with a lowercase letter, followed by letters, digits, dashes, or underscores.\n"
            "It cannot start or end with '-' or '_'."
        )
    return project_name


def _validate_username(username: str) -> str:
    """Validate and normalize a GitHub username.

    Args:
        username (str): The GitHub username to validate.

    Returns:
        str: The validated and stripped username.

    Raises:
        ValueError: If the username is empty.
    """
    if not username:
        raise ValueError("Username cannot be empty.")
    return username.strip()


def _validate_description(description: str) -> str:
    """Validate and normalize a project description.

    Args:
        description (str): The project description to validate.

    Returns:
        str: The validated and stripped description.

    Raises:
        ValueError: If the description is empty.
    """
    if not description:
        raise ValueError("Description cannot be empty.")
    return description.strip()


def _validate_page(page: str) -> str:
    """Validate and normalize a companion website URL.

    Args:
        page (str): The companion website URL to validate.

    Returns:
        str: The validated and stripped URL.

    Raises:
        ValueError: If the URL is empty.
    """
    if not page:
        raise ValueError("Page cannot be empty.")
    return page.strip()


def _validate_status(status: str) -> str:
    """Validate the repository visibility status.

    Args:
        status (str): The repository visibility status to validate.
            Must be one of: "public", "private", or "internal".

    Returns:
        str: The validated status.

    Raises:
        ValueError: If the status is not one of the valid options.
    """
    valid_statuses = {"public", "private", "internal"}
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}.")
    return status


def ask(logger: Optional[logging.Logger] = None, defaults: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """Collect and validate user input for GitHub repository creation.

    This function prompts the user for information needed to create a GitHub repository,
    including project name, username, description, companion website, and visibility status.
    It validates all inputs and returns a dictionary with the collected information and
    derived values like repository URL and SSH URI.

    Args:
        logger (Optional[logging.Logger], optional): Logger to use for logging messages.
            If None, a default logger will be created. Defaults to None.
        defaults (Optional[Dict[str, Any]], optional): Dictionary of default values to use
            for the prompts. Keys should match the keys in the returned dictionary.
            Defaults to None.

    Returns:
        Dict[str, str]: A dictionary containing the collected and validated information:
            - project_name: The name of the project
            - username: The GitHub username
            - description: The project description
            - status: The repository visibility status
            - ssh_uri: The SSH URI for the repository
            - repository: The HTTPS URL for the repository
            - gh_create: The GitHub CLI command to create the repository
            - page: The companion website URL
    """
    # Set up logger and defaults
    logger = logger or logging.getLogger(__name__)
    defaults = defaults or {}

    # --- Collect and validate user inputs ---

    # Project name: Must follow specific format rules
    # Get input with default from previous answers if available
    project_name = questionary.text("Enter your project name:", default=defaults.get("project_name", "")).ask()
    # Convert to lowercase and validate format
    project_name = _validate_project_name(project_name.lower())

    # GitHub username: Individual or organization name
    username = questionary.text(
        "Enter your GitHub username (e.g. 'tschm' or 'cvxgrp'):", default=defaults.get("username", "")
    ).ask()
    username = _validate_username(username)

    # Project description: Brief summary of the project
    description = questionary.text(
        "Enter a brief description of your project:", default=defaults.get("description", "")
    ).ask()
    description = _validate_description(description)

    # Companion website: Default to GitHub Pages URL if not specified
    # Note: We use the username and project_name collected above to build the default URL
    page = questionary.text(
        "Companion website:", default=defaults.get("page", f"https://{username}.github.io/{project_name}")
    ).ask()
    page = _validate_page(page)

    # Repository visibility: Use select for predefined choices
    # This ensures the user can only select valid options
    status = questionary.select(
        "What is the visibility status of the repository?",
        choices=["public", "private", "internal"],
        default=defaults.get("status", "public"),
    ).ask()
    status = _validate_status(status)

    # --- Generate derived values ---
    # These values are constructed from the validated inputs

    # Standard GitHub repository URL (HTTPS)
    repository_url = f"https://github.com/{username}/{project_name}"

    # SSH URI for Git operations (clone, push, pull)
    ssh_uri = f"git@github.com:{username}/{project_name}.git"

    # GitHub CLI command that could be used to create this repository
    gh_create = f"gh repo create {username}/{project_name} --{status} --description '{description}'"

    # --- Display summary to user ---
    # Show all collected and derived information for confirmation
    print("\n--- Repository Details ---")
    print(f"📌 Project Name: {project_name}")
    print(f"👤 GitHub Username: {username}")
    print(f"📝 Description: {description}")
    print(f"🔒 Visibility: {status}")
    print(f"🔗 Repository URL: {repository_url}")
    print(f"🌐 Companion Page: {page}")
    print(f"🔑 SSH URI: {ssh_uri}")
    print(f"🛠️ Command to create the repo: {gh_create}\n")

    # Log success
    logger.info("Repository details collected successfully.")

    # Return all collected and derived values as a dictionary
    # This will be used by other functions to create the repository
    return {
        "project_name": project_name,
        "username": username,
        "description": description,
        "status": status,
        "ssh_uri": ssh_uri,
        "repository": repository_url,
        "gh_create": gh_create,
        "page": page,
    }
