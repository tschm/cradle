from pathlib import Path

import pytest


@pytest.fixture()
def resource_dir():
    return Path(__file__).parent / "resources"
