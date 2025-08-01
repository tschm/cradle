"""Tests for the config module.

This module contains tests for the config.py module, which handles reading and writing
the configuration file, ensuring it exists, and getting template information.
"""

from pathlib import Path
from unittest.mock import mock_open, patch

from cradle.config import CONFIG_DIR, CONFIG_FILE, DEFAULT_CONFIG, _ensure_config_file, get_all_templates


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
    """Test that _ensure_config_file creates the directory and file if they don't exist."""
    # Setup
    mock_dir.exists.return_value = False
    mock_file.exists.return_value = False

    # Execute
    _ensure_config_file()

    # Assert
    mock_dir.mkdir.assert_called_once_with(parents=True)
    mock_open_file.assert_called_once_with(mock_file, "w")
    mock_open_file().write.assert_called()


@patch("cradle.config.CONFIG_DIR")
@patch("cradle.config.CONFIG_FILE")
@patch("builtins.open", new_callable=mock_open)
def test_ensure_config_file_creates_only_file(mock_open_file, mock_file, mock_dir):
    """Test that _ensure_config_file creates only the file if the directory exists."""
    # Setup
    mock_dir.exists.return_value = True
    mock_file.exists.return_value = False

    # Execute
    _ensure_config_file()

    # Assert
    mock_dir.mkdir.assert_not_called()
    mock_open_file.assert_called_once_with(mock_file, "w")
    mock_open_file().write.assert_called()


@patch("cradle.config.CONFIG_DIR")
@patch("cradle.config.CONFIG_FILE")
@patch("builtins.open", new_callable=mock_open)
def test_ensure_config_file_does_nothing(mock_open_file, mock_file, mock_dir):
    """Test that _ensure_config_file does nothing if the file exists."""
    # Setup
    mock_dir.exists.return_value = True
    mock_file.exists.return_value = True

    # Execute
    _ensure_config_file()

    # Assert
    mock_dir.mkdir.assert_not_called()
    mock_open_file.assert_not_called()


def test_get_all_templates_with_config_file(resource_dir):
    """Test that get_all_templates passes the config_file parameter to read_config."""
    templates = get_all_templates(config_file=resource_dir / "config.yml")
    assert set(templates.keys()) == {"experiments", "package", "paper"}
    assert templates == DEFAULT_CONFIG["templates"]


def test_get_all_templates_with_no_config_file():
    """Test that get_all_templates returns the default configuration if no config file is provided."""
    templates = get_all_templates(config_file=None)
    assert set(templates.keys()) == {"experiments", "package", "paper"}
    assert templates == DEFAULT_CONFIG["templates"]
