"""Global fixtures for cradle tests.

Security Notes:
- S101 (assert usage): Asserts are appropriate in test code for validating conditions
- S603/S607 (subprocess usage): Any subprocess calls use controlled inputs in test environments
"""

from pathlib import Path

import pytest


@pytest.fixture(scope="session", name="resource_dir")
def resource_fixture() -> Path:
    """Resource fixture."""
    return Path(__file__).parent / "resources"
