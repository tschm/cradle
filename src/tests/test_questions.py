"""Tests for the questions module."""

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
    """Test that _validate_project_name accepts valid project names.

    Verifies that the function returns the input name unchanged when given valid project names.
    """
    valid_names = ["project", "project123", "project_name", "a_very_long_project_name_123"]
    for name in valid_names:
        assert _validate_project_name(name) == name


def test_validate_project_name_invalid():
    """Test that _validate_project_name rejects invalid project names.

    Verifies that the function raises a ValueError when given invalid project names,
    such as empty strings, names with uppercase letters, names starting with numbers,
    names containing spaces, or names with special characters.
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
    """Test that _validate_username accepts valid usernames.

    Verifies that the function returns the input username unchanged when given valid usernames.
    """
    valid_usernames = ["user", "user123", "cvxgrp", "organization-name"]
    for username in valid_usernames:
        assert _validate_username(username) == username


def test_validate_username_invalid():
    """Test that _validate_username rejects invalid usernames.

    Verifies that the function raises a ValueError when given invalid usernames,
    such as empty strings or None values.
    """
    invalid_usernames = ["", None]
    for username in invalid_usernames:
        with pytest.raises(ValueError):
            _validate_username(username)


def test_validate_description_valid():
    """Test that _validate_description accepts valid descriptions.

    Verifies that the function returns the input description unchanged when given valid descriptions,
    including short descriptions and longer descriptions with multiple words.
    """
    valid_descriptions = ["A test project", "This is a longer description with multiple words", "Short desc"]
    for desc in valid_descriptions:
        assert _validate_description(desc) == desc


def test_validate_description_invalid():
    """Test that _validate_description rejects invalid descriptions.

    Verifies that the function raises a ValueError when given invalid descriptions,
    such as empty strings or None values.
    """
    invalid_descriptions = ["", None]
    for desc in invalid_descriptions:
        with pytest.raises(ValueError):
            _validate_description(desc)


def test_validate_status_valid():
    """Test that _validate_status accepts valid status values.

    Verifies that the function returns the input status unchanged when given valid status values
    (public, private, internal).
    """
    valid_statuses = ["public", "private", "internal"]
    for status in valid_statuses:
        assert _validate_status(status) == status


def test_validate_status_invalid():
    """Test that _validate_status rejects invalid status values.

    Verifies that the function raises a ValueError when given invalid status values,
    such as empty strings, None values, unrecognized status values, or status values
    with incorrect capitalization.
    """
    invalid_statuses = ["", None, "invalid", "PUBLIC", "Private"]
    for status in invalid_statuses:
        with pytest.raises(ValueError):
            _validate_status(status)


def test_validate_page_invalid():
    """Test that _validate_page rejects invalid page values.

    Verifies that the function raises a ValueError when given invalid page values,
    such as None values.
    """
    invalid_pages = [None]
    for page in invalid_pages:
        with pytest.raises(ValueError):
            _validate_page(page)


def test_ask_integration():
    """Integration test for the ask function.

    Tests that the ask function correctly processes user inputs and returns a properly
    formatted context dictionary with all expected keys and values. This test mocks
    the questionary.Question.ask method to simulate user inputs.
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
