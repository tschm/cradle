"""Tests for the updater GitHub Action.

This module contains tests that verify the updater action has the expected structure,
including required inputs, steps, and other elements. The updater action downloads
and extracts configuration templates from a GitHub repository.
"""

import os

import yaml


def test_updater_action_structure(action_path):
    """Test that the updater action has the expected structure."""
    # Path to the action.yml file
    updater_action_path = action_path("updater")

    # Ensure the file exists
    assert os.path.exists(updater_action_path), f"Action file not found at {updater_action_path}"

    # Load the action.yml file
    with open(updater_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "repository" in inputs, "Action must have repository input"
    assert "ref" in inputs, "Action must have ref input"

    # Check default values
    assert inputs["repository"]["default"] == "tschm/.config-templates", (
        "Repository input must default to tschm/.config-templates"
    )
    assert inputs["ref"]["default"] == "main", "Ref input must default to main"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 4, "Action must have at least 4 steps"

    # Check specific steps
    download_step = next((step for step in steps if step.get("name", "").startswith("Download")), None)
    assert download_step is not None, "Action must have a download templates step"

    extract_step = next((step for step in steps if step.get("name", "").startswith("Extract")), None)
    assert extract_step is not None, "Action must have an extract templates step"

    copy_step = next((step for step in steps if step.get("name", "").startswith("Copy")), None)
    assert copy_step is not None, "Action must have a copy templates step"

    cleanup_step = next((step for step in steps if step.get("name", "").startswith("Clean")), None)
    assert cleanup_step is not None, "Action must have a clean up step"

    # Check step details
    assert download_step["shell"] == "bash", "Download step must use bash shell"
    assert download_step["run"].find("${{ inputs.repository }}") != -1, "Download step must use repository input"
    assert download_step["run"].find("${{ inputs.ref }}") != -1, "Download step must use ref input"

    assert extract_step["shell"] == "bash", "Extract step must use bash shell"
    assert extract_step["run"].find("unzip templates.zip") != -1, "Extract step must unzip the templates"

    assert copy_step["shell"] == "bash", "Copy step must use bash shell"
    assert copy_step["run"].find("${{ inputs.repository }}") != -1, "Copy step must use repository input"
    assert copy_step["run"].find("${{ inputs.ref }}") != -1, "Copy step must use ref input"

    assert cleanup_step["shell"] == "bash", "Cleanup step must use bash shell"
    assert cleanup_step["run"].find("rm -rf templates.zip") != -1, "Cleanup step must remove the zip file"
