from unittest.mock import MagicMock

import pytest

from cvx.cradle.utils.git import GitNotFoundError, GitVersionError, _GitVersion, assert_git_version


def test_assert_git_version():
    assert_git_version(min_version="2.28.0")


def test_assert_git_version_tuple():
    assert_git_version(min_version=(2, 28, 0))


def test_assert_git_version_not_present():
    with pytest.raises(GitVersionError):
        assert_git_version(min_version="3.0.0")


def test_git_version():
    a = _GitVersion(2, 28, 0)
    with pytest.raises(TypeError):
        a >= 5


# Test when Git version is above the minimum required version
def test_check_git_version_success(mocker):
    # Mock subprocess.run to simulate a successful `git --version` output
    mocker.patch("subprocess.run", return_value=MagicMock(stdout="git version 2.34.1", returncode=0))

    min_version = "2.30.0"
    assert_git_version(min_version)

    # Assert that the function returns True since the version is >= 2.30.0
    # assert result is True


def test_check_git_version_invalid(mocker):
    # Mock subprocess.run to simulate a successful `git --version` output
    with pytest.raises(GitNotFoundError):
        mocker.patch("subprocess.run", return_value=MagicMock(stdout="Peter Maffay", returncode=1))

        min_version = "2.30.0"
        assert_git_version(min_version)


def test_check_git_version_invalid_str(mocker):
    # Mock subprocess.run to simulate a successful `git --version` output
    with pytest.raises(GitVersionError):
        mocker.patch("subprocess.run", return_value=MagicMock(stdout="git version 30", returncode=0))

        min_version = "2.30.0"
        assert_git_version(min_version)
