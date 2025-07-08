"""Tests for the cli module.

This module contains tests for the cli.py module, which provides the command-line
interface for qCradle, including commands for listing templates and creating projects.
"""

from unittest.mock import MagicMock, call, patch

import pytest
from rich.table import Table
from typer.testing import CliRunner

from cradle.cli import (
    app,
    create_project,
    get_available_templates,
    list_templates,
)


@pytest.fixture
def mock_templates():
    """Return a mock dictionary of templates."""
    return {
        "package": {
            "url": "https://github.com/tschm/package",
            "description": "Template for Python packages with PyPI publishing support",
        },
        "paper": {
            "url": "https://github.com/tschm/paper",
            "description": "Template for academic papers with LaTeX support",
        },
        "experiments": {
            "url": "https://github.com/tschm/experiments",
            "description": "Template for experimental projects with Marimo notebooks",
        },
    }


@pytest.fixture
def runner():
    """Return a CliRunner for testing Typer CLI applications."""
    return CliRunner()


@patch("cradle.cli.get_all_templates")
def test_get_available_templates(mock_get_all_templates, mock_templates):
    """Test that get_available_templates returns a sorted list of template names."""
    # Setup
    mock_get_all_templates.return_value = mock_templates

    # Execute
    result = get_available_templates()

    # Assert
    mock_get_all_templates.assert_called_once()
    assert result == ["experiments", "package", "paper"]


@patch("cradle.cli.get_all_templates")
@patch("cradle.cli.get_available_templates")
@patch("cradle.cli.console.print")
@patch("cradle.cli.rprint")
def test_list_templates_with_templates(
    mock_rprint, mock_console_print, mock_get_available_templates, mock_get_all_templates, mock_templates
):
    """Test that list_templates displays a table of templates when templates are available."""
    # Setup
    mock_get_all_templates.return_value = mock_templates
    mock_get_available_templates.return_value = ["experiments", "package", "paper"]

    # Execute
    list_templates()

    # Assert
    mock_get_all_templates.assert_called_once()
    mock_get_available_templates.assert_called_once()
    mock_rprint.assert_not_called()
    mock_console_print.assert_called_once()
    # Check that the argument to console.print is a Table
    assert isinstance(mock_console_print.call_args[0][0], Table)


@patch("cradle.cli.get_all_templates")
@patch("cradle.cli.get_available_templates")
@patch("cradle.cli.console.print")
@patch("cradle.cli.rprint")
def test_list_templates_no_templates(
    mock_rprint, mock_console_print, mock_get_available_templates, mock_get_all_templates
):
    """Test that list_templates displays an error message when no templates are available."""
    # Setup
    mock_get_all_templates.return_value = {}
    mock_get_available_templates.return_value = []

    # Execute
    list_templates()

    # Assert
    mock_get_all_templates.assert_called_once()
    mock_get_available_templates.assert_called_once()
    mock_rprint.assert_called_once_with("[bold red]No templates found![/bold red]")
    mock_console_print.assert_not_called()


@patch("cradle.cli.get_available_templates")
@patch("cradle.cli.get_template_info")
@patch("cradle.cli.rprint")
@patch("cradle.cli.sys.exit")
def test_create_project_success(
    mock_exit, mock_rprint, mock_get_template_info, mock_get_available_templates, mock_templates
):
    """Test that create_project creates a project successfully."""
    # Setup
    mock_get_available_templates.return_value = ["experiments", "package", "paper"]
    mock_get_template_info.return_value = mock_templates["package"]

    # Mock the copier module
    mock_copier = MagicMock()
    with patch.dict("sys.modules", {"copier": mock_copier}):
        # Execute
        create_project(template="package", project_name="test-project", description="Test project")

        # Assert
        mock_get_available_templates.assert_called_once()
        mock_get_template_info.assert_called_once_with("package")
        mock_rprint.assert_has_calls(
            [
                call("[bold]Creating project 'test-project' from template 'package'...[/bold]"),
                call("[bold]Using template URL: https://github.com/tschm/package[/bold]"),
                call("[bold green]Project created successfully at 'test-project'![/bold green]"),
            ]
        )
        mock_exit.assert_not_called()
        mock_copier.run_copy.assert_called_once_with(
            src_path="https://github.com/tschm/package",
            dst_path="test-project",
            data={
                "project_name": "test-project",
                "description": "Test project",
            },
            unsafe=True,
            defaults=True,
        )


def test_create_project_template_not_found(runner):
    """Test that create_project exits with an error when the template is not found."""
    with patch("cradle.cli.get_available_templates") as mock_get_available_templates:
        # Setup
        mock_get_available_templates.return_value = ["experiments", "package", "paper"]

        # Execute
        result = runner.invoke(
            app, ["create", "nonexistent", "--name", "test-project", "--description", "Test project"]
        )

        # Assert
        assert "Template 'nonexistent' not found!" in result.output
        assert "Available templates: experiments, package, paper" in result.output
        assert result.exit_code != 0


def test_create_project_no_url(runner):
    """Test that create_project exits with an error when the template has no URL."""
    with (
        patch("cradle.cli.get_available_templates") as mock_get_available_templates,
        patch("cradle.cli.get_template_info") as mock_get_template_info,
    ):
        # Setup
        mock_get_available_templates.return_value = ["experiments", "package", "paper"]
        # Return a dictionary without a URL key to simulate a template with no URL
        mock_get_template_info.return_value = {"description": "Template with no URL"}

        # Execute
        result = runner.invoke(app, ["create", "package", "--name", "test-project", "--description", "Test project"])

        # Assert
        assert "Template 'package' has no URL defined!" in result.output
        assert result.exit_code != 0


@patch("cradle.cli.get_available_templates")
@patch("cradle.cli.get_template_info")
@patch("cradle.cli.rprint")
@patch("cradle.cli.sys.exit")
def test_create_project_copier_error(
    mock_exit, mock_rprint, mock_get_template_info, mock_get_available_templates, mock_templates
):
    """Test that create_project handles errors from copier."""
    # Setup
    mock_get_available_templates.return_value = ["experiments", "package", "paper"]
    mock_get_template_info.return_value = mock_templates["package"]

    # Mock the copier module with an error
    mock_copier = MagicMock()
    mock_copier.run_copy.side_effect = Exception("Copier error")

    with patch.dict("sys.modules", {"copier": mock_copier}):
        # Execute
        create_project(template="package", project_name="test-project", description="Test project")

        # Assert
        mock_get_available_templates.assert_called_once()
        mock_get_template_info.assert_called_once_with("package")
        mock_rprint.assert_has_calls(
            [
                call("[bold]Creating project 'test-project' from template 'package'...[/bold]"),
                call("[bold]Using template URL: https://github.com/tschm/package[/bold]"),
                call("[bold red]Error creating project: Copier error[/bold red]"),
            ]
        )
        mock_exit.assert_called_once_with(1)


def test_app_commands():
    """Test that the app has the expected commands."""
    # Check that the app has the list and create commands
    command_names = [cmd.name for cmd in app.registered_commands]
    assert "list" in command_names
    assert "create" in command_names


def test_cli_runner_list(runner):
    """Test the list command using the CliRunner."""
    with (
        patch("cradle.cli.get_all_templates") as mock_get_all_templates,
        patch("cradle.cli.console.print") as mock_console_print,
    ):
        # Setup
        mock_get_all_templates.return_value = {
            "package": {
                "url": "https://github.com/tschm/package",
                "description": "Template for Python packages with PyPI publishing support",
            }
        }

        # Execute
        result = runner.invoke(app, ["list"])

        # Assert
        assert result.exit_code == 0
        # get_all_templates is called twice: once directly and once through get_available_templates
        assert mock_get_all_templates.call_count == 2
        mock_console_print.assert_called_once()


def test_cli_runner_create(runner):
    """Test the create command using the CliRunner."""
    with (
        patch("cradle.cli.get_available_templates") as mock_get_available_templates,
        patch("cradle.cli.get_template_info") as mock_get_template_info,
    ):
        # Setup
        mock_get_available_templates.return_value = ["package"]
        mock_get_template_info.return_value = {
            "url": "https://github.com/tschm/package",
            "description": "Template for Python packages with PyPI publishing support",
        }

        # Mock the copier module
        mock_copier = MagicMock()
        with patch.dict("sys.modules", {"copier": mock_copier}):
            # Execute
            result = runner.invoke(
                app, ["create", "package", "--name", "test-project", "--description", "Test project"]
            )

            # Assert
            assert result.exit_code == 0
            mock_get_available_templates.assert_called_once()
            mock_get_template_info.assert_called_once_with("package")
            mock_copier.run_copy.assert_called_once()
