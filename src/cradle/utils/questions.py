"""Questionary-based CLI questions and validation."""

import logging
import re

import questionary


def _validate_project_name(project_name):
    project_name = project_name.strip()
    if not re.match(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$", project_name):
        raise ValueError(
            "Project name must start with a lowercase letter, followed by letters, digits, dashes, or underscores.\n"
            "It cannot start or end with '-' or '_'."
        )
    return project_name


def _validate_username(username):
    if not username:
        raise ValueError("Username cannot be empty.")
    return username.strip()


def _validate_description(description):
    if not description:
        raise ValueError("Description cannot be empty.")
    return description.strip()


def ask(logger=None, defaults=None):
    """Prompt the user for project details and collect input, validate it, and log the repository information.

    This function interacts with the user to gather information required for creating a GitHub repository.

    Args:
        logger (Optional[logging.Logger]): Logger instance for logging messages.
        defaults (Optional[dict]): Dictionary containing default values for project details.

    Returns:
        dict: A dictionary containing the project details gathered from the user:
            - "project_name": The name of the project (str).
            - "username": The GitHub username (str).
            - "description": A brief description of the project (str).

    """
    logger = logger or logging.getLogger(__name__)
    defaults = defaults or {}

    # Get user inputs with questionary (use defaults from YAML)
    project_name = questionary.text("Enter your project name:", default=defaults.get("project_name", "")).ask()
    project_name = _validate_project_name(project_name.lower())

    username = questionary.text(
        "Enter your GitHub username (e.g. 'tschm' or 'cvxgrp'):", default=defaults.get("username", "")
    ).ask()
    username = _validate_username(username)

    description = questionary.text(
        "Enter a brief description of your project:", default=defaults.get("description", "")
    ).ask()
    description = _validate_description(description)

    # Display the results
    print("\n--- Repository Details ---")
    print(f"📌 Project Name: {project_name}")
    print(f"👤 GitHub Username: {username}")
    print(f"📝 Description: {description}")

    logger.info("Repository details collected successfully.")

    return {"project_name": project_name, "username": username, "description": description}
