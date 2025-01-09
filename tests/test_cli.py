import pytest

from cvx.cradle.cli import cli


def test_trivial(templates_dir, tmp_path):
    with pytest.raises(RuntimeError):
        cli(
            template=str(templates_dir / "experiments"),
            dst=tmp_path,
            user_defaults={"username": "Peter Maffay", "project_name": "test"},
        )
