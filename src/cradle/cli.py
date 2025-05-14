import datetime
import os
import shutil
import sys
import tempfile
from pathlib import Path

import copier
import questionary
import yaml
from fire import Fire
from loguru import logger

from .utils.gh_client import setup_repository
from .utils.git import assert_git_version
from .utils.questions import ask

# Add a new logger with a simpler format
logger.remove()  # Remove the default logger
logger.add(
    sys.stdout,
    colorize=True,  # Enable color output
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | {function}:{line} | <cyan>{message}</cyan>",
)


def load_templates(yaml_path: Path) -> dict[str, str]:
    """
    Load templates from YAML file and return a dictionary mapping display names to URLs.

    Args:
        yaml_path: Path to the YAML file containing template definitions

    Returns:
        dict[str, str]: Dictionary mapping template display names to their URLs
    """
    with open(yaml_path) as f:
        config = yaml.safe_load(f)

    return {details["display_name"]: details["url"] for template_name, details in config["templates"].items()}


def append_to_yaml_file(new_data, file_path):
    """
    Append new data to an existing YAML file or create a new one if it doesn't exist.

    Args:
        new_data: Dictionary containing data to append to the YAML file
        file_path: Path to the YAML file
    """
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing data from the file
        with open(file_path) as file:
            existing_data = yaml.safe_load(file) or {}  # Load existing data or empty dict if file is empty
    else:
        # If the file doesn't exist, start with an empty dict
        existing_data = {}

    # Append new data (update or add new keys)
    existing_data.update(new_data)

    # Write the updated data back to the YAML file
    with open(file_path, "w") as file:
        yaml.dump(existing_data, file, default_flow_style=False)


# Load defaults from .copier-answers.yml
def load_defaults(file_path=".copier-answers.yml"):
    """
    Load default values from a .copier-answers.yml file.

    Args:
        file_path: Path to the .copier-answers.yml file (default: ".copier-answers.yml")

    Returns:
        dict: Dictionary containing the default values from the YAML file or an empty dict if the file doesn't exist

    Raises:
        yaml.YAMLError: If there's an error parsing the YAML file
    """
    try:
        with open(file_path) as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}  # Return empty dict if the file is missing
    except yaml.YAMLError as e:
        print(f"⚠️ Error parsing YAML file: {e}")
        raise e


def cli(template: str = None, dst_path: str = None, vcs_ref: str | None = None, **kwargs) -> None:
    """
    The qCradle interface. Create GitHub repositories from the command line.
    It is also possible to create a large number of GitHub repositories.

    Args:
        template: optional (str) template. Use a git URI, e.g. 'git@...'.
                  Offers a group of standard templates to choose from if not specified.

        dst_path: optional (str) destination path. Useful when updating existing projects.
                  It has to be a full path. When given the template is ignored.

        vcs_ref: optional (str) revision number to checkout
                  a particular Git ref before generating the project.
    """

    # check the git version
    assert_git_version(min_version="2.28.0")

    # answer a bunch of questions
    logger.info("The qCradle will ask a group of questions to create a repository for you")

    # Store the original working directory to return to it later
    home = os.getcwd()

    # Branch based on whether we're creating a new project or updating an existing one
    if dst_path is None:
        # --- Creating a new project flow ---
        if template is None:
            # No template specified, so load the available templates and let the user choose
            yaml_path = Path(__file__).parent / "templates.yaml"  # Adjust path as needed
            templates = load_templates(yaml_path)

            # Present template choices to the user via interactive selection
            result = questionary.select(
                "What kind of project do you want to create?",
                choices=list(templates.keys()),
            ).ask()

            # Get the actual template URL from the selected display name
            template = templates[result]

        # For new projects, we'll use a temporary directory and clean it up later
        remove_path = True
        update = False
        dst_path = Path(tempfile.mkdtemp())
        logger.info(f"No destination path specified. Use {dst_path}")
        defaults = {}  # No defaults for new projects
        os.chdir(dst_path)

    else:
        # --- Updating an existing project flow ---
        logger.info(f"Destination path specified. Use {dst_path}")
        remove_path = False  # Don't remove the existing project directory
        update = True
        os.chdir(dst_path)

        # Load existing answers from the project to use as defaults
        defaults = load_defaults(".copier-answers.yml")

    # Collect user input for the project (with defaults if updating)
    context = ask(logger=logger, defaults=defaults)

    logger.info("*** Copier is parsing the template ***")

    # Apply the template based on whether we're updating or creating
    if update:
        # For updates, use copier's update functionality
        copier.run_update(dst_path, data=context, overwrite=True, **kwargs)

        # Create a timestamped branch for the update
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        branch = f"update-qcradle-{timestamp}"

        # Set up the Git repository with the update branch
        setup_repository(dst_path, context=context, branch=branch)
    else:
        # For new projects, copy the template to the destination
        copier.run_copy(template, dst_path, data=context, vcs_ref=vcs_ref, **kwargs)

        # Save the user's answers for future updates
        append_to_yaml_file(new_data=context, file_path=".copier-answers.yml")

        # Set up the Git repository with the main branch
        setup_repository(dst_path, context=context, branch="main")

    # --- Cleanup phase ---
    # Return to the original directory
    os.chdir(home)

    # If we created a temporary directory, remove it now that we're done with it
    # (The repository has been created on GitHub, so we don't need the local copy)
    if remove_path:
        shutil.rmtree(dst_path)

    # For new projects, remind the user they need to clone the repository
    if not update:
        logger.info(f"\n\nYou may have to perform 'git clone {context['ssh_uri']}'")


def main():  # pragma: no cover
    """
    Run the CLI using Fire
    """
    Fire(cli)
