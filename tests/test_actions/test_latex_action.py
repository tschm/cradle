"""Tests for the LaTeX GitHub Action.

This module contains tests that verify the LaTeX action has the expected structure,
including required inputs, steps, and other elements. The LaTeX action compiles
LaTeX documents to PDF using Tectonic and can deploy them to GitHub Pages.
"""

import os

import yaml


def test_latex_action_structure(action_path):
    """Test that the LaTeX action has the expected structure."""
    # Path to the action.yml file
    latex_action_path = action_path("latex")

    # Ensure the file exists
    assert os.path.exists(latex_action_path), f"Action file not found at {latex_action_path}"

    # Load the action.yml file
    with open(latex_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "tex-folder" in inputs, "Action must have tex-folder input"
    assert "tex-file" in inputs, "Action must have tex-file input"

    # Check default values
    assert inputs["tex-folder"]["default"] == "paper", "Tex-folder input must default to paper"
    assert inputs["tex-file"]["default"] == "document.tex", "Tex-file input must default to document.tex"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # The LaTeX action has a nested steps structure
    # First, check if steps is a dictionary with a 'steps' key (incorrect structure)
    steps = runs["steps"]["steps"] if isinstance(runs["steps"], dict) and "steps" in runs["steps"] else runs["steps"]

    assert len(steps) >= 3, "Action must have at least 3 steps"

    # Check specific steps
    install_step = None
    compile_step = None

    for step in steps:
        if isinstance(step, dict) and "name" in step:
            if step["name"].startswith("Install Tectonic"):
                install_step = step
            elif step["name"].startswith("Compile LaTeX"):
                compile_step = step

    assert install_step is not None, "Action must have an Install Tectonic step"
    assert compile_step is not None, "Action must have a Compile LaTeX document step"

    # Check step details
    assert "wtfjoke/setup-tectonic" in install_step["uses"], "Install step must use wtfjoke/setup-tectonic"
    assert "tectonic" in compile_step["run"], "Compile step must use tectonic"
