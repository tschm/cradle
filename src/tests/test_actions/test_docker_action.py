"""Tests for the docker GitHub Action.

This module contains tests that verify the docker action has the expected structure,
including required inputs, steps, and other elements. The docker action builds and
publishes Docker images using Podman/Buildah to a container registry.
"""

import os

import yaml


def test_docker_action_structure(action_path):
    """Test that the docker action has the expected structure."""
    # Path to the action.yml file
    docker_action_path = action_path("docker")

    # Ensure the file exists
    assert os.path.exists(docker_action_path), f"Action file not found at {docker_action_path}"

    # Load the action.yml file
    with open(docker_action_path) as f:
        action = yaml.safe_load(f)

    # Check basic structure
    assert "name" in action, "Action must have a name"
    assert "description" in action, "Action must have a description"
    assert "inputs" in action, "Action must have inputs"
    assert "runs" in action, "Action must have runs section"

    # Check inputs
    inputs = action["inputs"]
    assert "tag" in inputs, "Action must have tag input"
    assert "github_token" in inputs, "Action must have github_token input"
    assert "github_actor" in inputs, "Action must have github_actor input"
    assert "github_repository" in inputs, "Action must have github_repository input"
    assert "dockerfiles" in inputs, "Action must have dockerfiles input"
    assert "registry" in inputs, "Action must have registry input"
    assert "labels" in inputs, "Action must have labels input"

    # Check required inputs
    assert inputs["tag"]["required"] is True, "Tag input must be required"
    assert inputs["github_token"]["required"] is True, "GitHub token input must be required"
    assert inputs["github_actor"]["required"] is True, "GitHub actor input must be required"
    assert inputs["github_repository"]["required"] is True, "GitHub repository input must be required"

    # Check default values
    assert inputs["registry"]["default"] == "ghcr.io", "Registry input must default to ghcr.io"
    assert inputs["dockerfiles"]["default"] == "docker/Dockerfile", (
        "Dockerfiles input must default to docker/Dockerfile"
    )

    # Check runs section
    runs = action["runs"]
    assert runs["using"] == "composite", "Action must be a composite action"
    assert "steps" in runs, "Action must have steps"

    # Check steps
    steps = runs["steps"]
    assert len(steps) >= 3, "Action must have at least 3 steps"

    # Check specific steps
    login_step = next((step for step in steps if step.get("name", "").startswith("Log in")), None)
    assert login_step is not None, "Action must have a login step"

    build_step = next((step for step in steps if step.get("name", "").startswith("Build")), None)
    assert build_step is not None, "Action must have a build step"

    push_step = next((step for step in steps if step.get("name", "").startswith("Push")), None)
    assert push_step is not None, "Action must have a push step"

    # Check step details
    assert login_step["uses"] == "redhat-actions/podman-login@v1", "Login step must use redhat-actions/podman-login@v1"
    assert build_step["uses"] == "redhat-actions/buildah-build@v2", (
        "Build step must use redhat-actions/buildah-build@v2"
    )
    assert push_step["uses"] == "redhat-actions/push-to-registry@v2", (
        "Push step must use redhat-actions/push-to-registry@v2"
    )
