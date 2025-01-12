import dataclasses

import pytest

from cvx.cradle.cli import cli


@pytest.fixture
def mock_run_shell_command(mocker):
    """Fixture to mock `run_shell_command`."""
    # Mock run_shell_command and return a MagicMock so we can check calls
    return mocker.patch("cvx.cradle.cli.run_shell_command", autospec=True)


@pytest.fixture
def mock_context():
    return {
        "project_name": "Mocked Project",
        "username": "Jane Doe",
        "gh_create": "gh repo create mocked-project --private --confirm",
        "ssh_uri": "git@github.com:jane/mocked-project.git",
    }


@dataclasses.dataclass(frozen=True)
class Answer:
    string: str

    def ask(self):
        return self.string


def test_main(mock_context, mocker, tmp_path, mock_run_shell_command):
    mocker.patch("cvx.cradle.cli.ask", return_value=mock_context)

    cli(template="git@github.com:tschm/paper.git", dst_path=str(tmp_path))

    # Assert the correct number of calls (optional)
    assert mock_run_shell_command.call_count == 6


def test_no_template(mock_context, mocker, tmp_path, mock_run_shell_command):
    mocker.patch("cvx.cradle.cli.questionary.select", return_value=Answer("A paper"))
    mocker.patch("cvx.cradle.cli.ask", return_value=mock_context)

    cli(dst_path=str(tmp_path))


def test_runtime_error(mock_context, mocker, tmp_path):
    mocker.patch("cvx.cradle.cli.questionary.select", return_value=Answer("A paper"))
    mocker.patch("cvx.cradle.cli.ask", return_value=mock_context)
    mocker.patch("cvx.cradle.cli.run_shell_command", side_effect=RuntimeError("An error occurred"))

    with pytest.raises(RuntimeError):
        cli(dst_path=str(tmp_path))
