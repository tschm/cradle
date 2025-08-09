"""Tests for the deptry GitHub Action.

This module contains tests that verify the deptry action has the expected structure,
including required inputs, steps, and other elements. The deptry action analyzes
Python project dependencies for issues like unused, missing, and transitive dependencies.
"""

import os

import yaml


def test_deptry_action_structure(action_path):
    """Test that the deptry action has the expected structure."""
    # Path to the action.yml file
    deptry_action_path = action_path("deptry")

    # Ensure the file exists
    assert os.path.exists(deptry_action_path), f"Action file not found at {deptry_action_path}"

    # Load the action.yml file
    with open(deptry_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "source-folder" in inputs, "Action must have source-folder input"
    assert "options" in inputs, "Action must have options input"

    # Check required inputs
    assert inputs["source-folder"]["required"] is True, "Source-folder input must be required"

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

    uv_step = next((step for step in steps if step.get("name", "").startswith("Set up uv")), None)
    assert uv_step is not None, "Action must have a uv setup step"

    deptry_step = next((step for step in steps if step.get("name", "").startswith("Run Deptry")), None)
    assert deptry_step is not None, "Action must have a run deptry step"

    # Check deptry command
    assert deptry_step["run"].find("uvx deptry") != -1, "Deptry step must use uvx deptry command"
    assert deptry_step["run"].find("${{ inputs.source-folder }}") != -1, "Deptry step must use source-folder input"
    assert deptry_step["run"].find("${{ inputs.options }}") != -1, "Deptry step must use options input"
