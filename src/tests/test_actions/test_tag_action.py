"""Tests for the tag GitHub Action.

This module contains tests that verify the tag action has the expected structure,
including required inputs, outputs, steps, and other elements. The tag action
automatically bumps version numbers based on commit messages and creates releases.
"""

import os

import yaml


def test_tag_action_structure(action_path):
    """Test that the tag action has the expected structure."""
    # Path to the action.yml file
    tag_action_path = action_path("tag")

    # Ensure the file exists
    assert os.path.exists(tag_action_path), f"Action file not found at {tag_action_path}"

    # Load the action.yml file
    with open(tag_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "outputs" in action, "Action must have outputs"
    assert "runs" in action, "Action must have runs section"

    # Check outputs
    outputs = action["outputs"]
    assert "new_tag" in outputs, "Action must have new_tag output"
    assert outputs["new_tag"]["value"].find("steps.tag_version.outputs.new_tag") != -1, (
        "New tag output must reference tag_version step output"
    )

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 2, "Action must have at least 2 steps"

    # Check specific steps
    tag_step = next((step for step in steps if step.get("name", "").startswith("Bump version")), None)
    assert tag_step is not None, "Action must have a bump version and tag step"
    assert tag_step["id"] == "tag_version", "Bump version step must have id tag_version"

    release_step = next((step for step in steps if step.get("name", "").startswith("Create GitHub release")), None)
    assert release_step is not None, "Action must have a create GitHub release step"

    # Check step details
    assert tag_step["uses"] == "mathieudutour/github-tag-action@v6.2", (
        "Tag step must use mathieudutour/github-tag-action@v6.2"
    )

    assert release_step["uses"] == "softprops/action-gh-release@v2", (
        "Release step must use softprops/action-gh-release@v2"
    )
    assert release_step["with"]["tag_name"] == "${{ steps.tag_version.outputs.new_tag }}", (
        "Release step must use new_tag output from tag step"
    )
    assert release_step["with"]["generate_release_notes"] is True, "Release step must generate release notes"
