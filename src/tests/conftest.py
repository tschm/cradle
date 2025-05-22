from pathlib import Path

import pytest


@pytest.fixture()
def resource_dir():
    """
    Pytest fixture that provides the path to the test resources directory.

    Returns:
        Path: A Path object pointing to the resources directory within the tests folder.
    """
    return Path(__file__).parent / "resources"
