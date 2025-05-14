"""Tests for the questions module of the cradle project.

This module contains tests for the validation functions and the ask function
in the questions module, which are used to collect and validate user input
for project creation.
"""

from unittest.mock import patch

import pytest
import questionary

# Import the module with your functions
# Assuming the original code is in a file called project_setup.py
from cradle.utils.questions import (
    _validate_description,
    _validate_page,
    _validate_project_name,
    _validate_status,
    _validate_username,
    ask,
)


def test_validate_project_name_valid():
    """Test validation of valid project names.

    This test verifies that the _validate_project_name function correctly
    accepts valid project names and returns them unchanged.
    """
    valid_names = ["project", "project123", "project_name", "a_very_long_project_name_123"]
    for name in valid_names:
        assert _validate_project_name(name) == name


def test_validate_project_name_invalid():
    """Test validation of invalid project names.

    This test verifies that the _validate_project_name function correctly
    rejects invalid project names by raising a ValueError.
    """
    invalid_names = [
        "",  # empty
        "Project",  # uppercase
        "123project",  # starts with number
        "project name",  # space
        "@project",  # special character
    ]
    for name in invalid_names:
        with pytest.raises(ValueError):
            _validate_project_name(name)


def test_validate_username_valid():
    """Test validation of valid usernames.

    This test verifies that the _validate_username function correctly
    accepts valid usernames and returns them unchanged.
    """
    valid_usernames = ["user", "user123", "cvxgrp", "organization-name"]
    for username in valid_usernames:
        assert _validate_username(username) == username


def test_validate_username_invalid():
    """Test validation of invalid usernames.

    This test verifies that the _validate_username function correctly
    rejects invalid usernames by raising a ValueError.
    """
    invalid_usernames = ["", None]
    for username in invalid_usernames:
        with pytest.raises(ValueError):
            _validate_username(username)


def test_validate_description_valid():
    """Test validation of valid descriptions.

    This test verifies that the _validate_description function correctly
    accepts valid descriptions and returns them unchanged.
    """
    valid_descriptions = ["A test project", "This is a longer description with multiple words", "Short desc"]
    for desc in valid_descriptions:
        assert _validate_description(desc) == desc


def test_validate_description_invalid():
    """Test validation of invalid descriptions.

    This test verifies that the _validate_description function correctly
    rejects invalid descriptions by raising a ValueError.
    """
    invalid_descriptions = ["", None]
    for desc in invalid_descriptions:
        with pytest.raises(ValueError):
            _validate_description(desc)


def test_validate_status_valid():
    """Test validation of valid repository statuses.

    This test verifies that the _validate_status function correctly
    accepts valid repository statuses and returns them unchanged.
    """
    valid_statuses = ["public", "private", "internal"]
    for status in valid_statuses:
        assert _validate_status(status) == status


def test_validate_status_invalid():
    """Test validation of invalid repository statuses.

    This test verifies that the _validate_status function correctly
    rejects invalid repository statuses by raising a ValueError.
    """
    invalid_statuses = ["", None, "invalid", "PUBLIC", "Private"]
    for status in invalid_statuses:
        with pytest.raises(ValueError):
            _validate_status(status)


def test_validate_page_invalid():
    """Test validation of invalid page URLs.

    This test verifies that the _validate_page function correctly
    rejects invalid page URLs by raising a ValueError.
    """
    invalid_pages = [None]
    for page in invalid_pages:
        with pytest.raises(ValueError):
            _validate_page(page)


def test_ask_integration():
    """Test the integration of the ask function.

    This test verifies that the ask function correctly collects user input,
    validates it, and returns a properly formatted context dictionary with
    all the necessary information for project creation.
    """
    # Mock user inputs
    with patch.object(questionary.Question, "ask") as mock_ask:
        # Configure mock to return appropriate values for different questions
        mock_ask.side_effect = [
            "testproject",  # project name
            "testuser",  # username
            "Test description",  # description
            "https://testuser.github.io/testproject",
            "public",  # status
        ]

        result = ask()

        # Verify the returned context
        assert result["project_name"] == "testproject"
        assert result["username"] == "testuser"
        assert result["description"] == "Test description"
        assert result["status"] == "public"
        assert result["repository"] == "https://github.com/testuser/testproject"
        assert result["ssh_uri"] == "git@github.com:testuser/testproject.git"
        assert result["gh_create"] == "gh repo create testuser/testproject --public --description 'Test description'"
        assert result["page"] == "https://testuser.github.io/testproject"
