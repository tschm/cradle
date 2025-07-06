"""Tests for the environment GitHub Action.

This module contains tests that verify the environment action has the expected structure,
including required inputs, steps, and other elements. The environment action builds
a Python development environment using either pyproject.toml or requirements.txt.
"""

import os

import yaml


def test_environment_action_structure(action_path):
    """Test that the environment action has the expected structure."""
    # Path to the action.yml file
    environment_action_path = action_path("environment")

    # Ensure the file exists
    assert os.path.exists(environment_action_path), f"Action file not found at {environment_action_path}"

    # Load the action.yml file
    with open(environment_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "python-version" in inputs, "Action must have python-version input"
    assert "use-requirements-txt" in inputs, "Action must have use-requirements-txt input"
    assert "requirements-path" in inputs, "Action must have requirements-path input"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 3, "Action must have at least 3 steps"

    # Check specific steps
    checkout_step = next((step for step in steps if step.get("name", "").startswith("Checkout")), None)
    assert checkout_step is not None, "Action must have a checkout step"

    python_step = next((step for step in steps if step.get("name", "").startswith("Set up Python")), None)
    assert python_step is not None, "Action must have a Python setup step"

    # Check conditional steps for requirements.txt and pyproject.toml
    req_txt_step = next(
        (
            step
            for step in steps
            if step.get("if", "").find("use-requirements-txt") != -1 and step.get("if", "").find("true") != -1
        ),
        None,
    )
    assert req_txt_step is not None, "Action must have a step for requirements.txt"

    pyproject_step = next(
        (
            step
            for step in steps
            if step.get("if", "").find("use-requirements-txt") != -1 and step.get("if", "").find("false") != -1
        ),
        None,
    )
    assert pyproject_step is not None, "Action must have a step for pyproject.toml"
