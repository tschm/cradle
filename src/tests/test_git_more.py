"""Tests for the git_more module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import git

from cradle.utils.gh_client import GitHubCLI


def test_git(tmp_path: Path):
    """Test the functionality of initializing a Git repository.

    Adding a file, committing changes, and verifying the commit message.

    Args:
        tmp_path (Path): Pathlib Path object that provides a temporary
        directory for the test.

    Raises:
        AssertionError: If the commit message does not match the expected
        value.

    """
    repo_path = tmp_path / "myrepo"
    repo = git.Repo.init(repo_path)

    (repo_path / "test.txt").write_text("hello")
    repo.index.add(["test.txt"])
    repo.index.commit("initial commit")
    assert repo.head.commit.message == "initial commit"


@patch("cradle.utils.gh_client.safe_command.run")
def test_mock(mock_run, tmp_path: Path):
    """Test the `create_repo` method of the `GitHubCLI` class.

    By mocking the external
    `safe_command.run` function. Verifies that the mocked function is called once
    with the expected behavior and confirms the expected output.

    Args:
        mock_run (MagicMock): A mock object replacing the `safe_command.run` method
                              to observe and control its behavior.
        tmp_path (Path): A temporary directory path provided by pytest.

    Returns:
        None

    """
    mock_result = MagicMock()
    mock_result.stdout.strip.return_value = "repo created"
    mock_run.return_value = mock_result

    cli = GitHubCLI(verbose=False)
    output = cli.create_repo("test-user/repo-name", description="Test")

    assert output == "repo created"
    mock_run.assert_called_once()


@patch("cradle.utils.gh_client.safe_command.run")
def test_mock_verbose(mock_run, tmp_path: Path):
    """Mock the `run` command from the `cradle.utils.gh_client.safe_command` module.

    Validate the functionality of the verbose mode in the `create_repo` method
    of the `GitHubCLI` class.

    Parameters
    ----------
    mock_run : MagicMock
        The mock object for the `run` function.
    tmp_path : Path
        A temporary directory created for the test.

    Raises
    ------
    AssertionError
        If the `run` command is not called exactly once or if output does not match
        the expected result.

    """
    mock_result = MagicMock()
    mock_result.stdout.strip.return_value = "repo created"
    mock_run.return_value = mock_result

    cli = GitHubCLI(verbose=True)
    output = cli.create_repo("test-user/repo-name", description="Test")

    assert output is None
    mock_run.assert_called_once()
