"""Tests for the build GitHub Action.

This module contains tests that verify the build action has the expected structure,
including required inputs, steps, and other elements. The build action handles
building a Python package, updating the version, and creating a GitHub release.
"""

import os

import yaml


def test_build_action_structure(action_path):
    """Test that the build action has the expected structure."""
    # Path to the action.yml file
    build_action_path = action_path("build")

    # Ensure the file exists
    assert os.path.exists(build_action_path), f"Action file not found at {build_action_path}"

    # Load the action.yml file
    with open(build_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "tag" in inputs, "Action must have tag input"
    assert inputs["tag"]["required"] is True, "Tag input must be required"

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

    version_step = next((step for step in steps if step.get("name", "").startswith("Update version")), None)
    assert version_step is not None, "Action must have a version update step"

    build_step = next((step for step in steps if step.get("name", "").startswith("Build package")), None)
    assert build_step is not None, "Action must have a build step"

    upload_step = next((step for step in steps if step.get("name", "").startswith("Upload")), None)
    assert upload_step is not None, "Action must have an upload step"

    release_step = next((step for step in steps if step.get("name", "").startswith("Create GitHub release")), None)
    assert release_step is not None, "Action must have a release step"
