"""Tests for the CLI module."""

import dataclasses

import pytest
import yaml

from cradle.cli import append_to_yaml_file, cli, load_defaults

# @pytest.fixture
# def mock_run_shell_command(mocker):
#    """Fixture to mock `run_shell_command`."""
#    # Mock run_shell_command and return a MagicMock so we can check calls
#    return mocker.patch("cradle.cli.run_shell_command", autospec=True)


@pytest.fixture
def mock_context():
    """Pytest fixture that provides a mock context dictionary for testing.

    Returns:
        dict: A dictionary containing mock project information including project name,
              username, SSH URI, status, and description.

    """
    return {
        "project_name": "Mocked Project",
        "username": "Jane Doe",
        "ssh_uri": "git@github.com:jane/mocked-project.git",
        "status": "public",
        "description": "Mocked Project",
    }


@dataclasses.dataclass(frozen=True)
class Answer:
    """A mock class that simulates questionary's Answer objects for testing.

    Attributes:
        string (str): The string value to be returned when ask() is called.

    """

    string: str

    def ask(self):
        """Simulate the ask method of questionary's Answer objects.

        Returns:
            str: The string value stored in this Answer object.

        """
        return self.string


def test_no_template(mock_context, mocker):
    """Test the CLI functionality when no template is specified.

    Args:
        mock_context (dict): Fixture providing mock project context.
        mocker (pytest.MockFixture): Pytest fixture for mocking.

    """
    mocker.patch("cradle.cli.questionary.select", return_value=Answer("A LaTeX document"))
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_copy", return_value=None)
    mocker.patch("cradle.cli.setup_repository", return_value=None)
    cli(dst_path=None)
    # assert mock_run_shell_command.call_count == 6


def test_append_to_yaml_file(tmp_path):
    """Test the append_to_yaml_file function to ensure it correctly appends data to a YAML file.

    Args:
        tmp_path (Path): Pytest fixture providing a temporary directory path.

    """
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


def test_without_dst_path(mock_context, mocker):
    """Test the CLI functionality when no destination path is specified.

    Args:
        mock_context (dict): Fixture providing mock project context.
        mocker (pytest.MockFixture): Pytest fixture for mocking.

    """
    mocker.patch("cradle.cli.questionary.select", return_value=Answer("A LaTeX document"))
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_copy", return_value=None)
    mocker.patch("cradle.cli.setup_repository", return_value=None)
    cli()
    # assert mock_run_shell_command.call_count == 6


def test_load_defaults(resource_dir):
    """Test the load_defaults function with a valid file.

    Args:
        resource_dir (Path): Fixture providing the path to test resources.

    """
    data = load_defaults(resource_dir / ".copier-answers.yml")
    print(data)
    assert data["_src_path"] == "git@github.com:tschm/experiments.git"


def test_load_defaults_no_file(resource_dir):
    """Test the load_defaults function when the file doesn't exist.

    Args:
        resource_dir (Path): Fixture providing the path to test resources.

    """
    data = load_defaults(file_path=resource_dir / "maffay.yml")
    assert data == {}


# def test_load_broken(resource_dir):
#     """
#     Test the load_defaults function with a broken YAML file.
#
#     Args:
#         resource_dir (Path): Fixture providing the path to test resources.
#     """
#     with pytest.raises(YAMLError):
#         load_defaults(resource_dir / "broken.yml")


def test_update(tmp_path, mocker, mock_context):
    """Test the CLI update functionality.

    Args:
        tmp_path (Path): Pytest fixture providing a temporary directory path.
        mocker (pytest.MockFixture): Pytest fixture for mocking.
        mock_context (dict): Fixture providing mock project context.

    """
    # copy file resource_dir /.copier-answers into temp_dir
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_update", return_value=None)
    mocker.patch("cradle.cli.setup_repository", return_value=None)
    cli(dst_path=tmp_path)
