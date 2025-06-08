"""Command-line interface for qCradle."""

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

# from .utils.shell import run_shell_command

# Add a new logger with a simpler format
logger.remove()  # Remove the default logger
logger.add(
    sys.stdout,
    colorize=True,  # Enable color output
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | {function}:{line} | <cyan>{message}</cyan>",
)


def load_templates(yaml_path: Path) -> dict[str, str]:
    """Load templates from YAML file and return a dictionary mapping display names to URLs."""
    with open(yaml_path) as f:
        config = yaml.safe_load(f)

    return {details["display_name"]: details["url"] for template_name, details in config["templates"].items()}


def append_to_yaml_file(new_data, file_path):
    """Append or update a YAML file with new data.

    This function checks if the
    specified YAML file exists. If it exists, the current contents are loaded,
    updated with the new data, and written back to the file. If the file does not
    exist, a new file is created, and the provided data is written to it.

    Parameters
    ----------
    new_data : dict
        The new data to append to the YAML file. It should be a dictionary.
    file_path : str
        The path of the YAML file to update or create.

    Raises
    ------
    yaml.YAMLError
        If there is an error in parsing or dumping YAML data.
    IOError
        If there is an issue with file reading or writing.

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
    """Load default values from a specified YAML file.

    If the file is missing,
    it returns an empty dictionary. If the file is present but cannot be
    parsed due to invalid YAML formatting, an error message is printed and
    the exception is re-raised.

    Parameters
    ----------
    file_path: str
        The path to the YAML file from which defaults should be loaded. Defaults to
        ".copier-answers.yml".

    Returns
    -------
    dict
        A dictionary containing the parsed contents of the YAML file. If the file is
        not found, an empty dictionary is returned.

    Raises
    ------
    yaml.YAMLError
        If there is an error while parsing the YAML file, this exception is raised.

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
    """Create GitHub repositories from the command line.

    It is also possible to create a large number of GitHub repositories.

    Args:
        template: optional (str) template. Use a git URI, e.g. 'git@...'.
                  Offers a group of standard templates to choose from if not specified.

        dst_path: optional (str) destination path. Useful when updating existing projects.
                  It has to be a full path. When given the template is ignored.

        vcs_ref: optional (str) revision number to checkout
        a particular Git ref before generating the project.

        **kwargs: optional keyword arguments to pass to copier.run_copy() or copier.run_update()

    """
    # check the git version
    assert_git_version(min_version="2.28.0")

    # answer a bunch of questions
    logger.info("The qCradle will ask a group of questions to create a repository for you")

    home = os.getcwd()

    if dst_path is None:
        if template is None:
            # Load templates from YAML file
            yaml_path = Path(__file__).parent / "templates.yaml"  # Adjust path as needed
            templates = load_templates(yaml_path)

            # Let user select from the display names
            result = questionary.select(
                "What kind of project do you want to create?",
                choices=list(templates.keys()),
            ).ask()

            template = templates[result]
        remove_path = True
        update = False
        dst_path = Path(tempfile.mkdtemp())
        logger.info(f"No destination path specified. Use {dst_path}")
        defaults = {}
        os.chdir(dst_path)

    else:
        logger.info(f"Destination path specified. Use {dst_path}")
        remove_path = False
        update = True
        os.chdir(dst_path)

        defaults = load_defaults(".copier-answers.yml")

    context = ask(logger=logger, defaults=defaults)

    logger.info("*** Copier is parsing the template ***")

    # Copy material into the random path
    if update:
        copier.run_update(dst_path, data=context, overwrite=True, **kwargs)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        branch = f"update-qcradle-{timestamp}"

        setup_repository(dst_path, context=context, branch=branch)
        # Wrap with Repo object
        # repo = Repo(dst_path)
        # repo.git.checkout(branch)
        # repo.git.add(all=True)
        # repo.git.commit("-m", "Updates by qcradle")

        # Push to origin main
        # repo.remotes.origin.push(refspec=f"{branch}:{branch}")

    else:
        logger.info(f"{context}")
        copier.run_copy(template, dst_path, data=context, vcs_ref=vcs_ref, **kwargs)
        append_to_yaml_file(new_data=context, file_path=".copier-answers.yml")
        setup_repository(dst_path, context=context, branch="main")

    # go back to the repo
    os.chdir(home)

    # delete the path you have created
    if remove_path:
        shutil.rmtree(dst_path)

    if not update:
        logger.info(f"\n\nYou may have to perform 'git clone {context['ssh_uri']}'")


def main():  # pragma: no cover
    """Run the CLI using Fire."""
    Fire(cli)
