"""Tests for the Git and GitHub functionality of the cradle project.

This module contains tests for the Git and GitHub functionality, including
version checking, repository operations, and GitHub CLI integration.
"""

import subprocess
from unittest.mock import MagicMock, patch

import pytest
from git import InvalidGitRepositoryError, Repo

from cradle.utils.gh_client import GitHubCLI, is_git_repo, setup_repository


# Fixtures
@pytest.fixture
def mock_repo():
    """Provide a mock Git repository object.

    This fixture returns a MagicMock object that mimics a Git Repo object
    for testing purposes.

    Returns:
        MagicMock: A mock Git repository object.
    """
    return MagicMock(spec=Repo)


@pytest.fixture
def github_cli():
    """Provide a GitHubCLI instance for testing.

    This fixture returns a GitHubCLI instance with verbose mode disabled
    for cleaner test output.

    Returns:
        GitHubCLI: A GitHubCLI instance with verbose=False.
    """
    return GitHubCLI(verbose=False)


@pytest.fixture
def sample_context():
    """Provide a sample context dictionary for testing.

    This fixture returns a dictionary with sample project details
    that would normally be provided by user input.

    Returns:
        dict: A dictionary containing sample project details.
    """
    return {
        "username": "testuser",
        "project_name": "test-repo",
        "status": True,
        "description": "Test repository",
        "ssh_uri": "git@github.com:testuser/test-repo.git",
    }


# Test GitHubCLI
def test_github_cli_run_success(github_cli, mocker):
    """Test successful execution of GitHub CLI commands.

    This test verifies that the GitHubCLI.run method correctly handles
    successful command execution and returns the expected output.

    Args:
        github_cli: Fixture providing a GitHubCLI instance.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch("subprocess.run", return_value=MagicMock(stdout="success", stderr="", returncode=0))
    result = github_cli.run("repo", "list")
    assert result == "success"


def test_github_cli_run_failure(github_cli, mocker):
    """Test handling of GitHub CLI command failures.

    This test verifies that the GitHubCLI.run method correctly handles
    command failures by raising a RuntimeError with the appropriate message.

    Args:
        github_cli: Fixture providing a GitHubCLI instance.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "gh", stderr="Error"))
    with pytest.raises(RuntimeError, match="GitHub CLI error"):
        github_cli.run("invalid", "command")


def test_create_repo(github_cli, mocker):
    """Test repository creation with GitHub CLI.

    This test verifies that the GitHubCLI.create_repo method correctly
    constructs and executes the GitHub CLI command for creating a repository.

    Args:
        github_cli: Fixture providing a GitHubCLI instance.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch.object(github_cli, "run", return_value="Repository created")
    github_cli.create_repo("test/repo", private=True, description="Test")
    github_cli.run.assert_called_once_with(
        "repo", "create", "test/repo", "--private", "--description", "Test", "--confirm"
    )


# Test is_git_repo
def test_is_git_repo_valid(tmp_path, mock_repo):
    """Test is_git_repo with a valid Git repository.

    This test verifies that the is_git_repo function correctly identifies
    a valid Git repository by creating a .git directory and mocking the Repo.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.
        mock_repo: Fixture providing a mock Git repository object.
    """
    (tmp_path / ".git").mkdir()
    with patch("git.Repo", return_value=mock_repo):
        assert is_git_repo(tmp_path) is True


def test_is_git_repo_invalid(tmp_path):
    """Test is_git_repo with an invalid Git repository.

    This test verifies that the is_git_repo function correctly identifies
    a directory that is not a Git repository.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.
    """
    assert is_git_repo(tmp_path) is False


def test_is_git_repo_error(tmp_path, mocker):
    """Test is_git_repo when an InvalidGitRepositoryError is raised.

    This test verifies that the is_git_repo function correctly handles
    the case when an InvalidGitRepositoryError is raised.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch("git.Repo", side_effect=InvalidGitRepositoryError("Invalid"))
    assert is_git_repo(tmp_path) is False


def test_setup_repository_no_gh_cli(tmp_path, sample_context, mocker):
    """Test setup_repository when GitHub CLI is not installed.

    This test verifies that the setup_repository function correctly raises
    a RuntimeError when GitHub CLI is not installed.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.
        sample_context: Fixture providing a sample context dictionary.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch.object(GitHubCLI, "version", return_value=False)
    with pytest.raises(RuntimeError, match="GitHub is not installed"):
        setup_repository(tmp_path, sample_context)


# Test edge cases
def test_repo_name_with_spaces(github_cli, mocker):
    """Test repository creation with spaces in the name.

    This test verifies that the GitHubCLI.create_repo method correctly
    handles repository names with spaces by replacing them with hyphens.

    Args:
        github_cli: Fixture providing a GitHubCLI instance.
        mocker: Pytest fixture for mocking.
    """
    mocker.patch.object(github_cli, "run")
    github_cli.create_repo("test user/repo name", description="Test")
    github_cli.run.assert_called_once_with(
        "repo", "create", "test-user/repo-name", "--public", "--description", "Test", "--confirm"
    )
