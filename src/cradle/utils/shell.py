import logging
import subprocess


def run_shell_command(command: str, logger=None, **kwargs):
    """Run a shell command and handle errors"""
    logger = logger or logging.getLogger(__name__)

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, **kwargs)
        logger.info(f"Command succeeded: {command}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while running command `{command}`: {e.stderr.decode()}")
        raise RuntimeError(f"Error while running command `{command}`: {e.stderr.decode()}")
