import subprocess
from unittest.mock import MagicMock, patch

import pytest
from git import InvalidGitRepositoryError, Repo

from cradle.utils.gh_client import GitHubCLI, is_git_repo, setup_repository


# Fixtures
@pytest.fixture
def mock_repo():
    return MagicMock(spec=Repo)


@pytest.fixture
def github_cli():
    return GitHubCLI(verbose=False)


@pytest.fixture
def sample_context():
    return {
        "username": "testuser",
        "project_name": "test-repo",
        "status": True,
        "description": "Test repository",
        "ssh_uri": "git@github.com:testuser/test-repo.git",
    }


# Test GitHubCLI
def test_github_cli_run_success(github_cli, mocker):
    mocker.patch("subprocess.run", return_value=MagicMock(stdout="success", stderr="", returncode=0))
    result = github_cli.run("repo", "list")
    assert result == "success"


def test_github_cli_run_failure(github_cli, mocker):
    mocker.patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "gh", stderr="Error"))
    with pytest.raises(RuntimeError, match="GitHub CLI error"):
        github_cli.run("invalid", "command")


def test_create_repo(github_cli, mocker):
    mocker.patch.object(github_cli, "run", return_value="Repository created")
    github_cli.create_repo("test/repo", private=True, description="Test")
    github_cli.run.assert_called_once_with(
        "repo", "create", "test/repo", "--private", "--description", "Test", "--confirm"
    )


# Test is_git_repo
def test_is_git_repo_valid(tmp_path, mock_repo):
    (tmp_path / ".git").mkdir()
    with patch("git.Repo", return_value=mock_repo):
        assert is_git_repo(tmp_path) is True


def test_is_git_repo_invalid(tmp_path):
    assert is_git_repo(tmp_path) is False


def test_is_git_repo_error(tmp_path, mocker):
    mocker.patch("git.Repo", side_effect=InvalidGitRepositoryError("Invalid"))
    assert is_git_repo(tmp_path) is False


# # Test setup_repository
# def test_setup_new_repository(tmp_path, sample_context, mocker):
#     # Mock external dependencies
#     mocker.patch('cradle.utils.gh_client.is_git_repo', return_value=False)
#     mock_repo = MagicMock()
#     mock_repo.remotes = []
#     mocker.patch('git.Repo', return_value=mock_repo)
#     mocker.patch('git.Git.init')
#     mocker.patch.object(GitHubCLI, 'create_repo', return_value="Created")
#
#     # Test
#     repo = setup_repository(tmp_path, sample_context)
#
#     # Verify
#     GitHubCLI.create_repo.assert_called_once_with(
#         "testuser/test-repo", private=True, description="Test repository"
#     )
#     mock_repo.create_remote.assert_called_once_with(
#         "origin", "git@github.com:testuser/test-repo.git"
#     )
#     mock_repo.git.add.assert_called_once_with(A=True)
#     mock_repo.git.commit.assert_called_once_with(m="Initial commit by qcradle")
#     mock_repo.remotes.origin.push.assert_called_once_with(refspec="main:main")
#

# def test_setup_existing_repository(tmp_path, sample_context, mocker):
#     # Mock as existing repo
#     mocker.patch('cradle.utils.gh_client.is_git_repo', return_value=True)
#     mock_repo = MagicMock()
#     mock_repo.remotes = [MagicMock(name="origin")]
#     mocker.patch('git.Repo', return_value=mock_repo)
#
#     # Test
#     repo = setup_repository(tmp_path, sample_context)
#
#     # Verify
#     mock_repo.git.checkout.assert_called_once_with("main")
#     mock_repo.git.commit.assert_called_once_with(m="Update by qcradle")


def test_setup_repository_no_gh_cli(tmp_path, sample_context, mocker):
    mocker.patch.object(GitHubCLI, "version", return_value=False)
    with pytest.raises(RuntimeError, match="GitHub is not installed"):
        setup_repository(tmp_path, sample_context)


# Test edge cases
def test_repo_name_with_spaces(github_cli, mocker):
    mocker.patch.object(github_cli, "run")
    github_cli.create_repo("test user/repo name", description="Test")
    github_cli.run.assert_called_once_with(
        "repo", "create", "test-user/repo-name", "--public", "--description", "Test", "--confirm"
    )
