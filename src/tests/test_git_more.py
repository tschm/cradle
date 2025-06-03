from pathlib import Path
from unittest.mock import MagicMock, patch

import git

from cradle.utils.gh_client import GitHubCLI


def test_git(tmp_path: Path):
    repo_path = tmp_path / "myrepo"
    repo = git.Repo.init(repo_path)

    (repo_path / "test.txt").write_text("hello")
    repo.index.add(["test.txt"])
    repo.index.commit("initial commit")
    assert repo.head.commit.message == "initial commit"


@patch("cradle.utils.gh_client.safe_command.run")
def test_mock(mock_run, tmp_path: Path):
    mock_result = MagicMock()
    mock_result.stdout.strip.return_value = "repo created"
    mock_run.return_value = mock_result

    cli = GitHubCLI(verbose=False)
    output = cli.create_repo("test-user/repo-name", description="Test")

    assert output == "repo created"
    mock_run.assert_called_once()


@patch("cradle.utils.gh_client.safe_command.run")
def test_mock_verbose(mock_run, tmp_path: Path):
    mock_result = MagicMock()
    mock_result.stdout.strip.return_value = "repo created"
    mock_run.return_value = mock_result

    cli = GitHubCLI(verbose=True)
    output = cli.create_repo("test-user/repo-name", description="Test")

    assert output is None
    mock_run.assert_called_once()
