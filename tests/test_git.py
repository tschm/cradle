import pytest

from cvx.cradle.utils.git import GitVersionError, assert_git_version


def test_assert_git_version():
    assert_git_version(min_version="2.28.0")


def test_assert_git_version_not_present():
    with pytest.raises(GitVersionError):
        assert_git_version(min_version="3.0.0")
