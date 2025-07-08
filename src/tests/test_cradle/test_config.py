"""Tests for the config module.

This module contains tests for the config.py module, which handles reading and writing
the configuration file, ensuring it exists, and getting template information.
"""

from pathlib import Path
from unittest.mock import mock_open, patch

import yaml

from cradle.config import (
    CONFIG_DIR,
    CONFIG_FILE,
    DEFAULT_CONFIG,
    ensure_config_file,
    get_all_templates,
    get_template_info,
    read_config,
    write_config,
)


def test_config_constants():
    """Test that the config constants are correctly defined."""
    assert CONFIG_DIR == Path.home() / ".cradle"
    assert CONFIG_FILE == CONFIG_DIR / "config.yaml"
    assert "templates" in DEFAULT_CONFIG
    assert "experiments" in DEFAULT_CONFIG["templates"]
    assert "package" in DEFAULT_CONFIG["templates"]
    assert "paper" in DEFAULT_CONFIG["templates"]


@patch("cradle.config.CONFIG_DIR")
@patch("cradle.config.CONFIG_FILE")
@patch("builtins.open", new_callable=mock_open)
def test_ensure_config_file_creates_dir_and_file(mock_open_file, mock_file, mock_dir):
    """Test that ensure_config_file creates the directory and file if they don't exist."""
    # Setup
    mock_dir.exists.return_value = False
    mock_file.exists.return_value = False

    # Execute
    ensure_config_file()

    # Assert
    mock_dir.mkdir.assert_called_once_with(parents=True)
    mock_open_file.assert_called_once_with(mock_file, "w")
    mock_open_file().write.assert_called()


@patch("cradle.config.CONFIG_DIR")
@patch("cradle.config.CONFIG_FILE")
@patch("builtins.open", new_callable=mock_open)
def test_ensure_config_file_creates_only_file(mock_open_file, mock_file, mock_dir):
    """Test that ensure_config_file creates only the file if the directory exists."""
    # Setup
    mock_dir.exists.return_value = True
    mock_file.exists.return_value = False

    # Execute
    ensure_config_file()

    # Assert
    mock_dir.mkdir.assert_not_called()
    mock_open_file.assert_called_once_with(mock_file, "w")
    mock_open_file().write.assert_called()


@patch("cradle.config.CONFIG_DIR")
@patch("cradle.config.CONFIG_FILE")
@patch("builtins.open", new_callable=mock_open)
def test_ensure_config_file_does_nothing(mock_open_file, mock_file, mock_dir):
    """Test that ensure_config_file does nothing if the file exists."""
    # Setup
    mock_dir.exists.return_value = True
    mock_file.exists.return_value = True

    # Execute
    ensure_config_file()

    # Assert
    mock_dir.mkdir.assert_not_called()
    mock_open_file.assert_not_called()


@patch("cradle.config.ensure_config_file")
@patch("builtins.open", new_callable=mock_open, read_data=yaml.dump(DEFAULT_CONFIG))
def test_read_config(mock_open_file, mock_ensure_config):
    """Test that read_config reads the configuration file."""
    # Execute
    config = read_config()

    # Assert
    mock_ensure_config.assert_called_once()
    mock_open_file.assert_called_once_with(CONFIG_FILE)
    assert config == DEFAULT_CONFIG


@patch("cradle.config.ensure_config_file")
@patch("builtins.open", new_callable=mock_open)
def test_write_config(mock_open_file, mock_ensure_config):
    """Test that write_config writes to the configuration file."""
    # Setup
    config = {"test": "config"}

    # Execute
    write_config(config)

    # Assert
    mock_ensure_config.assert_called_once()
    mock_open_file.assert_called_once_with(CONFIG_FILE, "w")
    mock_open_file().write.assert_called()


@patch("cradle.config.read_config")
def test_get_template_info(mock_read_config):
    """Test that get_template_info returns information about a specific template."""
    # Setup
    mock_read_config.return_value = DEFAULT_CONFIG

    # Execute
    template_info = get_template_info("experiments")

    # Assert
    mock_read_config.assert_called_once()
    assert template_info == DEFAULT_CONFIG["templates"]["experiments"]


@patch("cradle.config.read_config")
def test_get_template_info_nonexistent(mock_read_config):
    """Test that get_template_info returns None for a nonexistent template."""
    # Setup
    mock_read_config.return_value = DEFAULT_CONFIG

    # Execute
    template_info = get_template_info("nonexistent")

    # Assert
    mock_read_config.assert_called_once()
    assert template_info is None


@patch("cradle.config.read_config")
def test_get_all_templates(mock_read_config):
    """Test that get_all_templates returns information about all templates."""
    # Setup
    mock_read_config.return_value = DEFAULT_CONFIG

    # Execute
    templates = get_all_templates()

    # Assert
    mock_read_config.assert_called_once()
    assert templates == DEFAULT_CONFIG["templates"]


@patch("cradle.config.read_config")
def test_get_all_templates_empty(mock_read_config):
    """Test that get_all_templates returns an empty dict if there are no templates."""
    # Setup
    mock_read_config.return_value = {}

    # Execute
    templates = get_all_templates()

    # Assert
    mock_read_config.assert_called_once()
    assert templates == {}
