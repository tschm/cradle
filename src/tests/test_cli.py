import dataclasses

import pytest
import yaml
from yaml import YAMLError

from cradle.cli import append_to_yaml_file, cli, load_defaults


@pytest.fixture
def mock_run_shell_command(mocker):
    """Fixture to mock `run_shell_command`."""
    # Mock run_shell_command and return a MagicMock so we can check calls
    return mocker.patch("cradle.cli.run_shell_command", autospec=True)


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


def test_no_template(mock_context, mocker, mock_run_shell_command):
    mocker.patch("cradle.cli.questionary.select", return_value=Answer("A LaTeX document"))
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_copy", return_value=None)
    cli(dst_path=None)
    assert mock_run_shell_command.call_count == 6


def test_runtime_error(mock_context, mocker):
    mocker.patch("cradle.cli.questionary.select", return_value=Answer("A LaTeX document"))
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_copy", return_value=None)
    mocker.patch("cradle.cli.run_shell_command", side_effect=RuntimeError("An error occurred"))

    with pytest.raises(RuntimeError):
        cli()


def test_append_to_yaml_file(tmp_path):
    data = {"A": 100, "B": 200}
    append_to_yaml_file(file_path=tmp_path / "a.yml", new_data=data)

    data = {"C": 300}
    append_to_yaml_file(file_path=tmp_path / "a.yml", new_data=data)

    # Read the file and verify the content
    with open(tmp_path / "a.yml") as f:
        content = yaml.safe_load(f)

    # Check that all data was correctly appended
    expected = {"A": 100, "B": 200, "C": 300}
    assert content == expected


def test_without_dst_path(mock_context, mocker, mock_run_shell_command):
    mocker.patch("cradle.cli.questionary.select", return_value=Answer("A LaTeX document"))
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_copy", return_value=None)
    cli()
    assert mock_run_shell_command.call_count == 6


def test_load_defaults(resource_dir):
    data = load_defaults(resource_dir / ".copier-answers.yml")
    print(data)
    assert data["_src_path"] == "git@github.com:tschm/experiments.git"


def test_load_defaults_no_file(resource_dir):
    data = load_defaults(file_path=resource_dir / "maffay.yml")
    assert data == {}


def test_load_broken(resource_dir):
    with pytest.raises(YAMLError):
        load_defaults(resource_dir / "broken.yml")


def test_update(tmp_path, mocker, mock_context, mock_run_shell_command):
    # copy file resource_dir /.copier-answers into temp_dir
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_update", return_value=None)

    cli(dst_path=tmp_path)

    assert mock_run_shell_command.call_count == 4
