#    Copyright 2023 Stanford University Convex Optimization Group
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
"""
cli to get weather data
"""

from pathlib import Path

import questionary
from copier import run_copy
from loguru import logger

from .git import assert_git_version

_templates = Path(__file__).parent / "templates"


def worker(template: str, dst_path, vcs_ref="HEAD", user_defaults=None):
    """Run copier to copy the template to the destination path"""
    if user_defaults is None:
        _worker = run_copy(src_path=template, dst_path=dst_path, vcs_ref=vcs_ref)
        return _worker

    # important for testing
    _worker = run_copy(
        src_path=template,
        dst_path=dst_path,
        vcs_ref=vcs_ref,
        unsafe=True,
        defaults=True,
        user_defaults=user_defaults,
    )

    return _worker


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
