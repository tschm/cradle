"""Tests for common functionality across all GitHub Actions.

This module contains tests that verify all GitHub Actions in the repository
have the required structure, good quality descriptions, and well-documented inputs.
These tests ensure consistency and quality across all actions.
"""

import os

import pytest
import yaml


def test_all_actions_exist(all_action_paths):
    """Test that all actions have an action.yml file."""
    assert len(all_action_paths) > 0, "No action.yml files found"

    # Check that we have tests for all actions
    for action_path in all_action_paths:
        action_name = os.path.basename(os.path.dirname(action_path))
        # Handle special case for pre-commit action (hyphen in name)
        if action_name == "pre-commit":
            test_file = os.path.join(os.path.dirname(__file__), "test_pre_commit_action.py")
        else:
            test_file = os.path.join(os.path.dirname(__file__), f"test_{action_name}_action.py")
        assert os.path.exists(test_file), f"No test file found for {action_name} action"


@pytest.mark.parametrize("action_file", ["all_action_paths"])
def test_action_basic_structure(action_file, all_action_paths, request):
    """Test that all actions have the required basic structure."""
    # Get the actual paths from the fixture if using the special 'all_action_paths' parameter
    paths = all_action_paths
    for path in paths:
        _test_action_basic_structure(path)


def _test_action_basic_structure(action_path):
    """Test a single action file."""
    # Load the action.yml file
    with open(action_path) as f:
        action = yaml.safe_load(f)

    action_name = os.path.basename(os.path.dirname(action_path))

    # Check basic structure
    assert "name" in action, f"{action_name} action must have a name"
    assert "description" in action, f"{action_name} action must have a description"
    assert "runs" in action, f"{action_name} action must have runs section"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", f"{action_name} action must be a composite action"
    assert "steps" in runs, f"{action_name} action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) > 0, f"{action_name} action must have at least one step"


@pytest.mark.parametrize("action_file", ["all_action_paths"])
def test_action_description_quality(action_file, all_action_paths, request):
    """Test that all actions have a good quality description."""
    # Get the actual paths from the fixture if using the special 'all_action_paths' parameter
    paths = all_action_paths
    for path in paths:
        _test_action_description_quality(path)


def _test_action_description_quality(action_path):
    """Test a single action file's description quality."""
    # Load the action.yml file
    with open(action_path) as f:
        action = yaml.safe_load(f)

    action_name = os.path.basename(os.path.dirname(action_path))

    # Check description quality
    assert "description" in action, f"{action_name} action must have a description"
    description = action["description"]
    assert len(description) >= 10, f"{action_name} action description must be at least 10 characters"
    assert description.strip() == description, (
        f"{action_name} action description must not have leading/trailing whitespace"
    )


@pytest.mark.parametrize("action_file", ["all_action_paths"])
def test_action_inputs_documentation(action_file, all_action_paths, request):
    """Test that all action inputs are well documented."""
    # Get the actual paths from the fixture if using the special 'all_action_paths' parameter
    paths = all_action_paths
    for path in paths:
        _test_action_inputs_documentation(path)


def _test_action_inputs_documentation(action_path):
    """Test a single action file's input documentation."""
    # Load the action.yml file
    with open(action_path) as f:
        action = yaml.safe_load(f)

    action_name = os.path.basename(os.path.dirname(action_path))

    # Skip if no inputs
    if "inputs" not in action:
        pytest.skip(f"{action_name} action has no inputs")

    # Check inputs documentation
    inputs = action["inputs"]
    for input_name, input_config in inputs.items():
        assert "description" in input_config, f"{action_name} action input {input_name} must have a description"
        description = input_config["description"]
        assert len(description) >= 5, (
            f"{action_name} action input {input_name} description must be at least 5 characters"
        )

        # Check if required is specified
        assert "required" in input_config, f"{action_name} action input {input_name} must specify if it's required"

        # If not required, should have a default value
        if input_config["required"] is False:
            assert "default" in input_config, (
                f"{action_name} action input {input_name} is not required but has no default value"
            )
