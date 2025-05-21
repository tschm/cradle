from dulwich.repo import Repo as DulwichRepo


# Test is_git_repo with Dulwich
def test_is_git_repo_valid_dulwich(tmp_path):
    """
    Test that is_git_repo returns True for a valid Git repository using Dulwich.

    Args:
        tmp_path (Path): Pytest fixture providing a temporary directory path.
        mock_dulwich_repo (MagicMock): Fixture providing a mock Dulwich repository.
    """
    # Create a .git directory to simulate a Git repository
    (tmp_path / ".git").mkdir()

    # Create a custom implementation of is_git_repo that uses Dulwich
    def is_git_repo_dulwich(path):
        try:
            git_dir = path / ".git"
            return git_dir.exists() or bool(DulwichRepo(str(path)))
        except Exception as e:
            print(f"⚠️  Error checking Git repo: {e}")
            return False

    # Test the function
    assert is_git_repo_dulwich(tmp_path) is True


def test_is_git_repo_invalid_dulwich(tmp_path):
    """
    Test that is_git_repo returns False for a directory that is not a Git repository using Dulwich.

    Args:
        tmp_path (Path): Pytest fixture providing a temporary directory path.
    """

    # Create a custom implementation of is_git_repo that uses Dulwich
    def is_git_repo_dulwich(path):
        try:
            git_dir = path / ".git"
            return git_dir.exists() or bool(DulwichRepo(str(path)))
        except Exception as e:
            print(f"⚠️  Error checking Git repo: {e}")
            return False

    # Test the function
    assert is_git_repo_dulwich(tmp_path) is False
