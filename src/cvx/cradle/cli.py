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

import copier
import fire
import questionary
from loguru import logger

from cvx.cradle.utils.questions import ask

from .utils.git import assert_git_version
from .utils.shell import run_shell_command


def cli(template: str = None, dst_path: str = None, vcs_ref: str | None = None, **kwargs) -> None:
    """
    The CRADLE command line interface. Create GitHub repositories with style.

    Args:
        template: optional (str) template. Use a git URI, e.g. 'git@...'
        dst_path: optional (str) destination path
        vcs_ref: optional (str) revision number
    """
    # check the git version
    assert_git_version(min_version="2.28.0")

    # answer a bunch of questions
    logger.info("cradle will ask a group of questions to create a repository for you")

    if template is None:
        # which template you want to pick?
        templates = {
            "(Marimo) Experiments": "git@github.com:tschm/experiments.git",
            "A package (complete with a release process)": "git@github.com:tschm/package.git",
            "A paper": "git@github.com:tschm/paper.git",
        }

        # result is the value related to the key you pick
        result = questionary.select(
            "What kind of project do you want to create?",
            choices=list(templates.keys()),
        ).ask()

        template = templates[result]

    # Create a random path
    dst_path = dst_path or Path(tempfile.mkdtemp())
    home = os.getcwd()
    # move into the folder used by the Factory
    os.chdir(dst_path)

    logger.info(f"Path to (re) construct your project: {dst_path}")

    context = ask()

    # Copy material into the random path
    copier.run_copy(template, dst_path, data=context, vcs_ref=vcs_ref, **kwargs)

    commands = [
        "git init --initial-branch=main",
        "git add --all",
        "git commit -m 'initial commit'",
        context["gh_create"],
        f"git remote add origin { context["ssh_uri"] }",
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

        logger.info(f"You may have to perform 'git clone { context["ssh_uri"] }'")


def main():  # pragma: no cover
    """
    Run the CLI using Fire
    """
    fire.Fire(cli)
