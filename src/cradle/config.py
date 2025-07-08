"""Configuration module for the Cradle CLI.

This module handles reading and writing the configuration file,
which contains information about available template repositories.
"""

from pathlib import Path
from typing import Any

import yaml

# Default configuration directory
CONFIG_DIR = Path.home() / ".cradle"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

# Default configuration
DEFAULT_CONFIG = {
    "templates": {
        "experiments": {
            "url": "https://github.com/tschm/cradle_templates/experiments",
            "description": "Template for experimental projects with Marimo notebooks",
        },
        "package": {
            "url": "https://github.com/tschm/cradle_templates/package",
            "description": "Template for Python packages with PyPI publishing support",
        },
        "paper": {
            "url": "https://github.com/tschm/cradle_templates/paper",
            "description": "Template for academic papers with LaTeX support",
        },
    }
}


def ensure_config_file() -> None:
    """Ensure the configuration file exists."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f)


def read_config() -> dict[str, Any]:
    """Read the configuration file."""
    ensure_config_file()

    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)


def write_config(config: dict[str, Any]) -> None:
    """Write the configuration file."""
    ensure_config_file()

    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f)


def get_template_info(template_name: str) -> dict[str, Any] | None:
    """Get information about a specific template."""
    config = read_config()
    return config.get("templates", {}).get(template_name)


def get_all_templates() -> dict[str, dict[str, Any]]:
    """Get information about all templates."""
    config = read_config()
    return config.get("templates", {})
