#    Copyright 2025 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import logging
import subprocess


def run_shell_command(command: str, logger=None):
    """Run a shell command and handle errors"""
    logger = logger or logging.getLogger(__name__)

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.info(f"Command succeeded: {command}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while running command `{command}`: {e.stderr.decode()}")
        raise RuntimeError(f"Error while running command `{command}`: {e.stderr.decode()}")
