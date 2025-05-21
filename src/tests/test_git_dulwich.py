from pathlib import Path

import git


def test_git(tmp_path: Path):
    repo_path = tmp_path / "myrepo"
    repo = git.Repo.init(repo_path)

    (repo_path / "test.txt").write_text("hello")
    repo.index.add(["test.txt"])
    repo.index.commit("initial commit")
    assert repo.head.commit.message == "initial commit"
