"""Tests for the pre-commit GitHub Action.

This module contains tests that verify the pre-commit action has the expected structure,
including required steps and other elements. The pre-commit action runs all configured
pre-commit hooks on all files in the repository to ensure code quality.
"""

import os

import yaml


def test_pre_commit_action_structure(action_path):
    """Test that the pre-commit action has the expected structure."""
    # Path to the action.yml file
    pre_commit_action_path = action_path("pre-commit")

    # Ensure the file exists
    assert os.path.exists(pre_commit_action_path), f"Action file not found at {pre_commit_action_path}"

    # Load the action.yml file
    with open(pre_commit_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "runs" in action, "Action must have runs section"

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

    node_step = next((step for step in steps if step.get("name", "").startswith("Install Node")), None)
    assert node_step is not None, "Action must have a Node.js setup step"

    pre_commit_step = next((step for step in steps if step.get("uses", "").startswith("pre-commit/action")), None)
    assert pre_commit_step is not None, "Action must have a pre-commit step"

    # Check step details
    assert checkout_step["uses"] == "actions/checkout@v6", "Checkout step must use actions/checkout@v4"
    assert node_step["uses"] == "actions/setup-node@v6", "Node step must use actions/setup-node@v6"
    assert node_step["with"]["node-version"] == "24", "Node step must use Node.js version 22"
    assert pre_commit_step["uses"] == "pre-commit/action@v3.0.1", "Pre-commit step must use pre-commit/action@v3.0.1"
    assert pre_commit_step["with"]["extra_args"] == "--verbose --all-files", (
        "Pre-commit step must run on all files with verbose output"
    )
