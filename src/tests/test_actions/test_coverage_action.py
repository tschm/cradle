"""Tests for the coverage GitHub Action.

This module contains tests that verify the coverage action has the expected structure,
including required inputs, steps, and other elements. The coverage action runs tests
with comprehensive coverage reporting and optional Coveralls integration.
"""

import os

import yaml


def test_coverage_action_structure(action_path):
    """Test that the coverage action has the expected structure."""
    # Path to the action.yml file
    coverage_action_path = action_path("coverage")

    # Ensure the file exists
    assert os.path.exists(coverage_action_path), f"Action file not found at {coverage_action_path}"

    # Load the action.yml file
    with open(coverage_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "tests-folder" in inputs, "Action must have tests-folder input"
    assert "source-folder" in inputs, "Action must have source-folder input"

    # Check required inputs
    assert inputs["tests-folder"]["required"] is True, "Tests-folder input must be required"
    assert inputs["source-folder"]["required"] is True, "Source-folder input must be required"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 2, "Action must have at least 2 steps"

    # Check specific steps
    run_tests_step = next((step for step in steps if step.get("name", "").startswith("Run tests with coverage")), None)
    assert run_tests_step is not None, "Action must have a run tests with coverage step"

    upload_results_step = next((step for step in steps if step.get("name", "").startswith("Upload test results")), None)
    assert upload_results_step is not None, "Action must have an upload test results step"
