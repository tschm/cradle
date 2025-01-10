import os

import pytest

from cvx.cradle.utils.ui import worker


@pytest.fixture(name="worker")
def worker_fixture(tmp_path, templates_dir):
    return worker(
        template=str(templates_dir / "experiments"),
        dst_path=tmp_path,
        user_defaults={"project_name": "test", "username": "PeterMaffay"},
    )


def test_dst_path(worker):
    for file in os.listdir(worker.dst_path):
        print(file)


def test_command(worker):
    command = worker.answers.user["command"]
    assert (
        command
        == "gh repo create PeterMaffay/test --public --description 'Some computations'"
    )
