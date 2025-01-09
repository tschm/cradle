from cvx.cradle.utils.shell import run_shell_command


def test_shell():
    results = run_shell_command("git --version")
    assert results.returncode == 0


def test_shell_bad_command():
    results = run_shell_command("Peter Maffay")
    assert results is None
