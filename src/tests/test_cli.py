"""Tests for the CLI module of the cradle project.

This module contains tests for the CLI functionality, including command-line
interface functions, YAML file operations, and repository setup.
"""

import dataclasses

import pytest
import yaml
from yaml import YAMLError

from cradle.cli import append_to_yaml_file, cli, load_defaults


@pytest.fixture
def mock_context():
    """Provide a mock context dictionary for testing.

    This fixture returns a dictionary with mock values for project details
    that would normally be provided by user input.

    Returns:
        dict: A dictionary containing mock project details.
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
    """A mock class that mimics questionary's answer objects.

    This class is used to mock the behavior of questionary's answer objects
    in tests, providing a simple way to simulate user input.

    Attributes:
        string: The string value that will be returned when ask() is called.
    """

    string: str

    def ask(self):
        """Simulate the ask method of questionary objects.

        Returns:
            str: The string value stored in this Answer object.
        """
        return self.string


def test_no_template(mock_context, mocker, tmp_path):
    """Test the CLI function when no template is specified.

    This test verifies that the CLI function works correctly when no template
    is specified, by mocking the necessary dependencies and checking that
    the function executes without errors.

    Args:
        mock_context: Fixture providing mock project context.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch("cradle.cli.questionary.select", return_value=Answer("A LaTeX document"))
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_copy", return_value=None)
    mocker.patch("cradle.cli.setup_repository", return_value=None)
    assert cli(dst_path=None) is None


def test_append_to_yaml_file(tmp_path):
    """Test the append_to_yaml_file function.

    This test verifies that the append_to_yaml_file function correctly
    appends new data to an existing YAML file, or creates a new file
    if it doesn't exist.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.
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
    """Test the CLI function when no destination path is specified.

    This test verifies that the CLI function works correctly when called
    without specifying a destination path, by mocking the necessary
    dependencies and checking that the function executes without errors.

    Args:
        mock_context: Fixture providing mock project context.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch("cradle.cli.questionary.select", return_value=Answer("A LaTeX document"))
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_copy", return_value=None)
    mocker.patch("cradle.cli.setup_repository", return_value=None)
    assert cli() is None


def test_load_defaults(resource_dir):
    """Test loading default values from a .copier-answers.yml file.

    This test verifies that the load_defaults function correctly loads
    default values from a .copier-answers.yml file.

    Args:
        resource_dir: Fixture providing the path to the resources directory.
    """
    data = load_defaults(resource_dir / ".copier-answers.yml")
    assert data["_src_path"] == "git@github.com:tschm/experiments.git"


def test_load_defaults_no_file(resource_dir):
    """Test loading default values when the file doesn't exist.

    This test verifies that the load_defaults function returns an empty
    dictionary when the specified file doesn't exist.

    Args:
        resource_dir: Fixture providing the path to the resources directory.
    """
    data = load_defaults(file_path=resource_dir / "maffay.yml")
    assert data == {}


def test_load_broken(resource_dir):
    """Test loading default values from a broken YAML file.

    This test verifies that the load_defaults function raises a YAMLError
    when trying to load a broken YAML file.

    Args:
        resource_dir: Fixture providing the path to the resources directory.
    """
    with pytest.raises(YAMLError):
        load_defaults(resource_dir / "broken.yml")


def test_update(tmp_path, mocker, mock_context):
    """Test the CLI function when updating an existing project.

    This test verifies that the CLI function works correctly when updating
    an existing project, by mocking the necessary dependencies and checking
    that the function executes without errors.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.
        mocker: Pytest fixture for mocking.
        mock_context: Fixture providing mock project context.
    """
    # copy file resource_dir /.copier-answers into temp_dir
    mocker.patch("cradle.cli.ask", return_value=mock_context)
    mocker.patch("cradle.cli.copier.run_update", return_value=None)
    mocker.patch("cradle.cli.setup_repository", return_value=None)
    cli(dst_path=tmp_path)
