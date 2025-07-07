"""Tests for the latex GitHub Action.

This module contains tests that verify the latex action has the expected structure,
including required inputs, steps, and other elements. The latex action compiles
LaTeX documents to PDF using Tectonic and can deploy them to GitHub Pages.
"""

import os

import yaml


def test_latex_action_structure(action_path):
    """Test that the latex action has the expected structure."""
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
    assert "paper" in inputs, "Action must have paper input"
    assert "output-folder" in inputs, "Action must have output-folder input"
    assert "draft" in inputs, "Action must have draft input"

    # Check required inputs
    assert inputs["paper"]["required"] is True, "Paper input must be required"

    # Check default values
    assert inputs["output-folder"]["default"] == "compiled", "Output-folder input must default to compiled"
    assert inputs["draft"]["default"] == "draft", "Draft input must default to draft"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 8, "Action must have at least 8 steps"

    # Check specific steps
    checkout_step = next((step for step in steps if step.get("name", "").startswith("Set up Git")), None)
    assert checkout_step is not None, "Action must have a checkout step"

    env_step = next((step for step in steps if step.get("name", "").startswith("Setup environment")), None)
    assert env_step is not None, "Action must have an environment setup step"

    dir_step = next((step for step in steps if step.get("name", "").startswith("Create output")), None)
    assert dir_step is not None, "Action must have a create output directories step"

    validate_step = next((step for step in steps if step.get("name", "").startswith("Validate")), None)
    assert validate_step is not None, "Action must have a validate input files step"

    install_step = next((step for step in steps if step.get("name", "").startswith("Install Tectonic")), None)
    assert install_step is not None, "Action must have an install Tectonic step"

    compile_step = next((step for step in steps if step.get("name", "").startswith("Compile LaTeX")), None)
    assert compile_step is not None, "Action must have a compile LaTeX documents step"

    deploy_step = next((step for step in steps if step.get("name", "").startswith("Deploy to GitHub")), None)
    assert deploy_step is not None, "Action must have a deploy to GitHub Pages step"

    upload_step = next((step for step in steps if step.get("name", "").startswith("Upload build")), None)
    assert upload_step is not None, "Action must have an upload build artifacts step"
