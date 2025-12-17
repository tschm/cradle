"""Command-line interface for qCradle."""

import sys

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from .config import get_all_templates

# Initialize Typer app
app = typer.Typer(
    name="qCradle",
    help="CLI tool for generating projects using Copier templates from configured repositories",
    add_completion=False,
)

# Initialize Rich console
console = Console()


@app.command("list")
def list_templates():
    """List all available templates."""
    template_configs = get_all_templates()
    template_names = sorted(template_configs.keys())

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
    description: str = typer.Option(
        "A project created with Cradle CLI", "--description", "-d", help="Project description"
    ),
    user_name: str = typer.Option(..., "--username", "-u", help="GitHub username for repository URL"),
    visibility: str = typer.Option(
        "private",
        "--visibility",
        "-v",
        help="Visibility of the GitHub repository: private, public, or internal",
    ),
):
    """Create a new project from a template."""
    template_configs = get_all_templates()
    available_templates = sorted(template_configs.keys())

    if template not in available_templates:
        rprint(f"[bold red]Template '{template}' not found![/bold red]")
        rprint(f"Available templates: {', '.join(available_templates)}")
        sys.exit(1)

    # Get template information from config
    template_info = template_configs.get(template, None)

    if not template_info or "url" not in template_info:
        rprint(f"[bold red]Template '{template}' has no URL defined![/bold red]")
        sys.exit(1)

    template_url = template_info["url"]

    output_dir = project_name

    # Prepare data for copier
    data = {
        "project_name": project_name,
        "description": description,
        "username": user_name,
        "repository": f"https://github.com/{user_name}/{project_name}",
    }

    # Import copier here to avoid slow startup time
    import copier

    try:
        rprint(f"[bold]Creating project '{project_name}' from template '{template}'...[/bold]")
        rprint(f"[bold]Using template URL: {template_url}[/bold]")
        rprint(f"[bold green]Copying template to '{output_dir}'...[/bold green]")

        # Run copier with the template URL
        copier.run_copy(
            src_path=template_url,
            dst_path=output_dir,
            data=data,
            unsafe=True,
            defaults=True,
        )

        rprint(f"[bold green]Project created successfully at '{output_dir}'![/bold green]")
        rprint("To create the project on GitHub, run the following commands in your terminal:")
        rprint("")
        rprint(f"""
        gh repo create --{visibility} {user_name}/{project_name} --description '{description}'
        cd {output_dir}
        git init
        git add .
        git commit -m "first commit"
        git branch -M main
        git remote add origin git@github.com:{user_name}/{project_name}.git
        git push -u origin main
        uvx rhiza validate
        uvx rhiza materialize
        """)

    except Exception as e:
        rprint(f"[bold red]Error creating project: {e}[/bold red]")
        sys.exit(1)


@app.callback()
def callback():
    """Cradle CLI - A command-line interface for generating projects using Copier templates.

    Templates are defined in a configuration file (~/.cradle/config.yaml) that maps
    template names to repository URLs.
    """
    pass


def main():
    """Entry point for the CLI."""
    app()  # pragma: no cover
