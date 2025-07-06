"""Tests for the book GitHub Action.

This module contains tests that verify the book action has the expected structure,
including required inputs, steps, and other elements. The book action creates
a minibook from a list of links and deploys it to GitHub Pages.
"""

import os

import yaml


def test_book_action_structure(action_path):
    """Test that the book action has the expected structure."""
    # Path to the action.yml file
    book_action_path = action_path("book")

    # Ensure the file exists
    assert os.path.exists(book_action_path), f"Action file not found at {book_action_path}"

    # Load the action.yml file
    with open(book_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "title" in inputs, "Action must have title input"
    assert "subtitle" in inputs, "Action must have subtitle input"
    assert "links" in inputs, "Action must have links input"
    assert "template" in inputs, "Action must have template input"

    # Check required inputs
    assert inputs["links"]["required"] is True, "Links input must be required"

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 6, "Action must have at least 6 steps"

    # Check specific steps
    python_step = next((step for step in steps if step.get("name", "").startswith("Set up Python")), None)
    assert python_step is not None, "Action must have a Python setup step"

    download_step = next((step for step in steps if step.get("name", "").startswith("Download all")), None)
    assert download_step is not None, "Action must have a download artifacts step"

    create_step = next((step for step in steps if step.get("name", "").startswith("Create minibook")), None)
    assert create_step is not None, "Action must have a create minibook step"

    inspect_step = next((step for step in steps if step.get("name", "").startswith("Inspect")), None)
    assert inspect_step is not None, "Action must have an inspect artifacts step"

    upload_step = next((step for step in steps if step.get("name", "").startswith("Upload")), None)
    assert upload_step is not None, "Action must have an upload step"

    deploy_step = next((step for step in steps if step.get("name", "").startswith("Deploy")), None)
    assert deploy_step is not None, "Action must have a deploy step"
