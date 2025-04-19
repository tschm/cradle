import logging
import shlex
import subprocess

from security import safe_command


def run_shell_command(command: str, logger=None, **kwargs):
    """Run a shell command and handle errors"""
    logger = logger or logging.getLogger(__name__)

    if isinstance(command, str):
        command = shlex.split(command)

    try:
        result = safe_command.run(
            subprocess.run, command, shell=False, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
        )
        logger.info(f"Command succeeded: {command}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while running command `{command}`: {e.stderr.decode()}")
        raise RuntimeError(f"Error while running command `{command}`: {e.stderr.decode()}")
