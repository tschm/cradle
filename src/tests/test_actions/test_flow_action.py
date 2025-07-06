"""Tests for the flow GitHub Action.

This module contains tests that verify the flow action has the expected structure,
including required inputs, steps, and other elements. The flow action tests
GitHub workflow files locally using the act tool.
"""

import os

import yaml


def test_flow_action_structure(action_path):
    """Test that the flow action has the expected structure."""
    # Path to the action.yml file
    flow_action_path = action_path("flow")

    # Ensure the file exists
    assert os.path.exists(flow_action_path), f"Action file not found at {flow_action_path}"

    # Load the action.yml file
    with open(flow_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "workflow" in inputs, "Action must have workflow input"
    assert "working-directory" in inputs, "Action must have working-directory input"

    # Check required inputs
    assert inputs["workflow"]["required"] is True, "Workflow input must be required"

    # Check default values
    assert inputs["working-directory"]["default"] == "template", "Working-directory input must default to template"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 3, "Action must have at least 3 steps"

    # Check specific steps
    install_step = next((step for step in steps if step.get("name", "").startswith("Install act")), None)
    assert install_step is not None, "Action must have an install act step"

    verify_step = next((step for step in steps if step.get("name", "").startswith("Verify act")), None)
    assert verify_step is not None, "Action must have a verify act installation step"

    test_step = next((step for step in steps if step.get("name", "").startswith("Test workflow")), None)
    assert test_step is not None, "Action must have a test workflow step"

    # Check step details
    assert install_step["run"].find("curl") != -1, "Install step must use curl to download act"
    assert verify_step["run"].find("act --version") != -1, "Verify step must check act version"
    assert test_step["run"].find("act -W") != -1, "Test step must use act -W to run workflow"
    assert test_step["working-directory"] == "${{ inputs.working-directory }}", (
        "Test step must use working-directory input"
    )
