"""global fixtures"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session", name="root")
def root_fixture():
    """resource fixture"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session", name="templates_dir")
def templates_fixture(root):
    """global fixtures for resources"""
    return root / "cvx" / "cradle" / "templates"


@pytest.fixture(scope="session", name="template")
def template_fixture(templates_dir):
    def f(name):
        return str(templates_dir / name)

    return f
