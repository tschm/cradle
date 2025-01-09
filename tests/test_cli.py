import pytest

from cvx.cradle.cli import cli


def test_experiments(templates_dir, tmp_path):
    with pytest.raises(RuntimeError):
        cli(
            template=str(templates_dir / "experiments"),
            dst=str(tmp_path),
            user_defaults={"username": "Peter Maffay", "project_name": "test"},
        )


def test_paper(templates_dir, tmp_path):
    with pytest.raises(RuntimeError):
        cli(
            template=str(templates_dir / "paper"),
            dst=str(tmp_path),
            user_defaults={"username": "Peter Maffay", "project_name": "test"},
        )


def test_package(templates_dir, tmp_path):
    with pytest.raises(RuntimeError):
        cli(
            template=str(templates_dir / "package"),
            dst=str(tmp_path),
            user_defaults={"username": "Peter Maffay", "project_name": "test"},
        )
