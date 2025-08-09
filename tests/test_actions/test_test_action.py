"""Tests for the test GitHub Action.

This module contains tests that verify the test action has the expected structure,
including required inputs, steps, and other elements. The test action provides
a simple way to run pytest tests with a configurable test directory.
"""

import os

import yaml


def test_test_action_structure(action_path):
    """Test that the test action has the expected structure."""
    # Path to the action.yml file
    test_action_path = action_path("test")

    # Ensure the file exists
    assert os.path.exists(test_action_path), f"Action file not found at {test_action_path}"

    # Load the action.yml file
    with open(test_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "tests-folder" in inputs, "Action must have tests-folder input"

    # Check default values
    assert inputs["tests-folder"]["default"] == "tests", "Tests-folder input must default to tests"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 1, "Action must have at least 1 step"

    # Check specific steps
    run_tests_step = next((step for step in steps if step.get("name", "").startswith("Run tests")), None)
    assert run_tests_step is not None, "Action must have a run tests step"

    # Check step details
    assert run_tests_step["shell"] == "${{ runner.os == 'Windows' && 'pwsh' || 'bash' }}", (
        "Run tests step must use cross-platform shell selection"
    )
    assert run_tests_step["run"].find("uv pip install") != -1, "Run tests step must install pytest"
    assert run_tests_step["run"].find("uv run pytest") != -1, "Run tests step must run pytest"
    assert run_tests_step["run"].find("${{ inputs.tests-folder }}") != -1, "Run tests step must use tests-folder input"
