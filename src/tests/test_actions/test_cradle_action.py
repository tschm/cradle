"""Tests for the cradle GitHub Action.

This module contains tests that verify the cradle action has the expected structure,
including required inputs, steps, and other elements. The cradle action sets up
a new project using the cradle template with copier.
"""

import os

import yaml


def test_cradle_action_structure(action_path):
    """Test that the cradle action has the expected structure."""
    # Path to the action.yml file
    cradle_action_path = action_path("cradle")

    # Ensure the file exists
    assert os.path.exists(cradle_action_path), f"Action file not found at {cradle_action_path}"

    # Load the action.yml file
    with open(cradle_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "python-version" in inputs, "Action must have python-version input"
    assert "destination-path" in inputs, "Action must have destination-path input"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 6, "Action must have at least 6 steps"

    # Check specific steps
    checkout_step = next((step for step in steps if step.get("name", "").startswith("Checkout")), None)
    assert checkout_step is not None, "Action must have a checkout step"

    python_step = next((step for step in steps if step.get("name", "").startswith("Set up Python")), None)
    assert python_step is not None, "Action must have a Python setup step"

    install_step = next((step for step in steps if step.get("name", "").startswith("Update pip")), None)
    assert install_step is not None, "Action must have an install copier step"

    git_step = next((step for step in steps if step.get("name", "").startswith("Prepare git")), None)
    assert git_step is not None, "Action must have a prepare git step"

    copier_step = next((step for step in steps if step.get("name", "").startswith("Run copier")), None)
    assert copier_step is not None, "Action must have a run copier step"

    repo_step = next((step for step in steps if step.get("name", "").startswith("Prepare the repo")), None)
    assert repo_step is not None, "Action must have a prepare repo step"
