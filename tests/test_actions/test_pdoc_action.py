"""Tests for the pdoc GitHub Action.

This module contains tests that verify the pdoc action has the expected structure,
including required inputs, steps, and other elements. The pdoc action generates
API documentation from Python source code using pdoc.
"""

import os

import yaml


def test_pdoc_action_structure(action_path):
    """Test that the pdoc action has the expected structure."""
    # Path to the action.yml file
    pdoc_action_path = action_path("pdoc")

    # Ensure the file exists
    assert os.path.exists(pdoc_action_path), f"Action file not found at {pdoc_action_path}"

    # Load the action.yml file
    with open(pdoc_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "source-folder" in inputs, "Action must have source-folder input"
    assert "pdoc-arguments" in inputs, "Action must have pdoc-arguments input"

    # Check default values
    assert inputs["source-folder"]["default"] == "cvx", "Source-folder input must default to cvx"
    assert inputs["pdoc-arguments"]["default"] == "", "Pdoc-arguments input must default to empty string"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 2, "Action must have at least 2 steps"

    # Check specific steps
    build_step = next((step for step in steps if step.get("name", "").startswith("Install and build")), None)
    assert build_step is not None, "Action must have an install and build pdoc step"

    upload_step = next((step for step in steps if step.get("name", "").startswith("Upload")), None)
    assert upload_step is not None, "Action must have an upload documentation step"

    # Check step details
    assert build_step["run"].find("uv pip install pdoc") != -1, "Build step must install pdoc"
    assert build_step["run"].find("uv run pdoc") != -1, "Build step must run pdoc"
    assert build_step["run"].find("${{ inputs.pdoc-arguments }}") != -1, "Build step must use pdoc-arguments input"
    assert build_step["run"].find("${{ inputs.source-folder }}") != -1, "Build step must use source-folder input"
