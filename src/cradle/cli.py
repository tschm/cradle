"""Command-line interface for qCradle."""

import sys

import typer
from loguru import logger
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from .config import get_all_templates, get_template_info

# Add a new logger with a simpler format
logger.remove()  # Remove the default logger
logger.add(
    sys.stdout,
    colorize=True,  # Enable color output
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | {function}:{line} | <cyan>{message}</cyan>",
)

# Initialize Typer app
app = typer.Typer(
    name="qCradle",
    help="CLI tool for generating projects using Copier templates from configured repositories",
    add_completion=False,
)

# Create a subcommand for template management
# template_app = typer.Typer(
#   name="template", help="Manage template repositories in the configuration file (~/.cradle/config.yaml)"
# )

# Add the template subcommand to the main app
# app.add_typer(template_app, name="template")

# Initialize Rich console
console = Console()


def get_available_templates() -> list[str]:
    """Get a list of available templates from the configuration."""
    templates = get_all_templates()
    return sorted(templates.keys())


@app.command("list")
def list_templates():
    """List all available templates."""
    template_configs = get_all_templates()
    template_names = get_available_templates()

    if not template_names:
        rprint("[bold red]No templates found![/bold red]")
        return

    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("URL", style="blue")

    for name in template_names:
        template_info = template_configs[name]
        description = template_info.get("description", "No description available")
        url = template_info.get("url", "")
        table.add_row(name, description, url)

    console.print(table)


@app.command("create")
def create_project(
    template: str = typer.Argument(..., help="Template to use"),
    project_name: str = typer.Option(..., "--name", "-n", help="Name of the project"),
    # output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory"),
    # username: str = typer.Option(os.environ.get("USER", "user"), "--username", "-u", help="Your username"),
    description: str = typer.Option(
        "A project created with Cradle CLI", "--description", "-d", help="Project description"
    ),
    # repository: str = typer.Option("", "--repository", "-r", help="Repository URL"),
):
    """Create a new project from a template."""
    templates = get_available_templates()

    if template not in templates:
        rprint(f"[bold red]Template '{template}' not found![/bold red]")
        rprint(f"Available templates: {', '.join(templates)}")
        sys.exit(1)

    # Get template information from config
    template_info = get_template_info(template)
    if not template_info or "url" not in template_info:
        rprint(f"[bold red]Template '{template}' has no URL defined![/bold red]")
        sys.exit(1)

    template_url = template_info["url"]

    # if output_dir is None:
    output_dir = project_name

    # Prepare data for copier
    data = {
        "project_name": project_name,
        # "username": username,
        "description": description,
        # "repository": repository,
    }

    # Import copier here to avoid slow startup time
    import copier

    try:
        rprint(f"[bold]Creating project '{project_name}' from template '{template}'...[/bold]")
        rprint(f"[bold]Using template URL: {template_url}[/bold]")

        # Run copier with the template URL
        copier.run_copy(
            src_path=template_url,
            dst_path=output_dir,
            data=data,
            unsafe=True,
            defaults=True,
        )

        rprint(f"[bold green]Project created successfully at '{output_dir}'![/bold green]")
    except Exception as e:
        rprint(f"[bold red]Error creating project: {e}[/bold red]")
        sys.exit(1)


@app.callback()
def callback():
    """Cradle CLI - A command-line interface for generating projects using Copier templates.

    Templates are defined in a configuration file (~/.cradle/config.yaml) that maps
    template names to repository URLs. Use the 'template' subcommand to manage templates.
    """
    pass


def main():
    """Entry point for the CLI."""
    app()  # pragma: no cover
