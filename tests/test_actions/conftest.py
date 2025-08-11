"""Pytest fixtures for GitHub Actions tests.

This module provides fixtures for accessing GitHub Actions in the repository,
including paths to the repository root, actions directory, and action.yml files.
These fixtures simplify path handling in the test files.
"""

import glob
import os

import pytest


@pytest.fixture
def repo_root():
    """Return the path to the repository root."""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def actions_dir(repo_root):
    """Return the path to the actions directory."""
    return os.path.join(repo_root, "actions")


@pytest.fixture
def action_path(actions_dir):
    """Return a function that returns the path to a specific action."""

    def _action_path(action_name):
        """Return the path to the action.yml file for the given action."""
        return os.path.join(actions_dir, action_name, "action.yml")

    return _action_path


@pytest.fixture
def all_action_paths(actions_dir):
    """Return a list of paths to all action.yml files."""
    return glob.glob(os.path.join(actions_dir, "*", "action.yml"))
