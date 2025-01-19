#    Copyright 2025 Stanford University Convex Optimization Group
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
import os
import shutil
import tempfile
from pathlib import Path

import copier
import questionary
import yaml
from fire import Fire
from loguru import logger

from cvx.cradle.utils.questions import ask

from .utils.git import assert_git_version
from .utils.shell import run_shell_command


def load_templates(yaml_path: Path) -> dict[str, str]:
    """
    Load templates from YAML file and return a dictionary mapping display names to URLs.
    """
    with open(yaml_path) as f:
        config = yaml.safe_load(f)

    return {details["display_name"]: details["url"] for template_name, details in config["templates"].items()}


def append_to_yaml_file(new_data, file_path):
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


def cli(template: str = None, dst_path: str = None, vcs_ref: str | None = None, **kwargs) -> None:
    """
    The CRADLE interface. Create GitHub repositories from the command line.
    It is also possible to create a large number of GitHub repositories.

    Args:
        template: optional (str) template. Use a git URI, e.g. 'git@...'.
                  Offers a group of standard templates to choose from if not specified.

        dst_path: optional (str) destination path. Useful when updating existing projects.

        vcs_ref: optional (str) revision number to checkout
        a particular Git ref before generating the project.
    """

    # check the git version
    assert_git_version(min_version="2.28.0")

    # answer a bunch of questions
    logger.info("cradle will ask a group of questions to create a repository for you")

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
    remove_path = False
    # Create a random path
    if not dst_path:
        remove_path = True

    dst_path = dst_path or Path(tempfile.mkdtemp())
    home = os.getcwd()
    # move into the folder used by the Factory
    os.chdir(dst_path)

    logger.info(f"Path to (re) construct your project: {dst_path}")

    context = ask(logger=logger)
    logger.info("*** Copier is parsing the template ***")
    # Copy material into the random path
    copier.run_copy(template, dst_path, data=context, vcs_ref=vcs_ref, **kwargs)

    logger.info("*** Create a file with the answers given ***\n")
    append_to_yaml_file(context, ".copier-answers.yml")

    commands = [
        "git init --initial-branch=main",
        "git add --all",
        "git commit -m 'initial commit by the Cradle'",
        context["gh_create"],
        f"git remote add origin {context['ssh_uri']}",
        "git push origin main",
    ]

    try:
        for cmd in commands:
            run_shell_command(cmd, logger=logger)

    except RuntimeError as e:
        logger.error(f"Failed to create project: {str(e)}")
        raise

    finally:
        # go back to the repo
        os.chdir(home)

        # delete the path you have created
        if remove_path:
            shutil.rmtree(dst_path)

        logger.info(f"\n\nYou may have to perform 'git clone {context['ssh_uri']}'")


def main():  # pragma: no cover
    """
    Run the CLI using Fire
    """
    Fire(cli)
