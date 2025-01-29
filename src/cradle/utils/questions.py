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


def _validate_page(page):
    if not page:
        raise ValueError("Page cannot be empty.")
    return page.strip()


def _validate_status(status):
    valid_statuses = {"public", "private", "internal"}
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}.")
    return status


def ask(logger=None, defaults=None):
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

    page = questionary.text(
        "Companion website:", default=defaults.get("page", f"https://{username}.github.io/{project_name}")
    ).ask()
    page = _validate_page(page)

    status = questionary.select(
        "What is the visibility status of the repository?",
        choices=["public", "private", "internal"],
        default=defaults.get("status", "public"),
    ).ask()
    status = _validate_status(status)

    # Generate dynamic values
    repository_url = f"https://github.com/{username}/{project_name}"
    ssh_uri = f"git@github.com:{username}/{project_name}.git"
    gh_create = f"gh repo create {username}/{project_name} --{status} --description '{description}'"

    # Display the results
    print("\n--- Repository Details ---")
    print(f"📌 Project Name: {project_name}")
    print(f"👤 GitHub Username: {username}")
    print(f"📝 Description: {description}")
    print(f"🔒 Visibility: {status}")
    print(f"🔗 Repository URL: {repository_url}")
    print(f"🌐 Companion Page: {page}")
    print(f"🔑 SSH URI: {ssh_uri}")
    print(f"🛠️ Command to create the repo: {gh_create}\n")

    logger.info("Repository details collected successfully.")

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
