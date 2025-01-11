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
import tempfile
from pathlib import Path

import questionary
from loguru import logger

from .utils.git import assert_git_version
from .utils.shell import run_shell_command
from .utils.ui import worker

_templates = Path(__file__).parent / "templates"


def cli(template: str = None, dst: str = None, vcs_ref: str = "HEAD", user_defaults=None) -> None:
    """
    CLI for Factory

    Args:
        template: (optional) template. Use a git URI, e.g. 'git@...'
        dst: (optional) destination. Use a path
    """
    # check the git version
    assert_git_version(min_version="2.28.0")

    # answer a bunch of questions
    logger.info("cradle will ask a group of questions to create a repository for you")

    if template is None:
        # which template you want to pick?
        templates = {
            "(Marimo) Experiments": str(_templates / "experiments"),
            "A package (complete with a release process)": str(_templates / "package"),
            "A paper": str(_templates / "paper"),
        }

        # result is the value related to the key you pick
        result = questionary.select(
            "What kind of project do you want to create?",
            choices=list(templates.keys()),
        ).ask()

        template = templates[result]

    # Create a random path
    path = dst or Path(tempfile.mkdtemp())
    home = os.getcwd()
    # move into the folder used by the Factory
    os.chdir(path)

    logger.info(f"Path to (re)construct your project: {path}")

    # Copy material into the random path
    _worker = worker(template=template, dst_path=path, vcs_ref=vcs_ref, user_defaults=user_defaults)

    command = _worker.answers.user["command"]
    ssh_uri = _worker.answers.user["ssh_uri"]
    # print(_worker.answers.user)

    commands = [
        "git init --initial-branch=main",
        "git add --all",
        "git commit -m 'initial commit'",
        command,
        f"git remote add origin {ssh_uri}",
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

        logger.info(f"You may have to perform 'git clone {ssh_uri}'")
