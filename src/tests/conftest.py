"""Test configuration and fixtures for the cradle project.

This module contains pytest fixtures that are available to all tests.
"""

from pathlib import Path

import pytest


@pytest.fixture()
def resource_dir():
    """Return the path to the resources directory.

    This fixture provides access to test resources located in the 'resources'
    directory relative to this file.

    Returns:
        Path: Path object pointing to the resources directory.
    """
    return Path(__file__).parent / "resources"
