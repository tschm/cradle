# GitHub Actions Tests

This directory contains tests for all
GitHub Actions in the repository.
The tests ensure that the actions have
the expected structure, inputs, and steps.

## Test Files

- `test_all_actions.py`: Tests common functionality
across all actions, such as basic structure, description quality,
and input documentation.
- Individual test files for each action
(e.g., `test_environment_action.py`, `test_build_action.py`, etc.):
Test the specific structure and functionality of each action.
- `conftest.py`: Contains fixtures for the path to actions,
making it easier to write and maintain tests.

## Running the Tests

To run all the tests for the actions:

```bash
cd src
python -m pytest tests/actions -v
```

To run tests for a specific action:

```bash
cd src
python -m pytest tests/actions/test_environment_action.py -v
```

## Test Coverage

The tests cover the following aspects of the actions:

1. **Basic Structure**: Ensures that each action has the
required fields (name, description, runs) and is a composite
action with steps.
2. **Description Quality**: Checks that the action description
is of good quality (at least 10 characters, no leading/trailing
whitespace).
3. **Input Documentation**: Verifies that all inputs are
well documented (have a description of at least 5 characters,
specify if they're required, and have a default value if not required).
4. **Action-Specific Structure**: Tests the specific structure
and functionality of each action, including required inputs,
default values, and specific steps.

## Fixtures

The `conftest.py` file provides the following fixtures
to make it easier to write and maintain tests:

- `repo_root`: Returns the path to the repository root.
- `actions_dir`: Returns the path to the actions directory.
- `action_path`: Returns a function that returns the path
to a specific action's action.yml file.
- `all_action_paths`: Returns a list of paths to all action.yml files.

### Using the Fixtures

Here's an example of how to use the fixtures in a test:

```python
def test_my_action_structure(action_path):
    """Test that the my-action has the expected structure."""
    # Get the path to the action.yml file
    my_action_path = action_path('my-action')

    # Ensure the file exists
    assert os.path.exists(my_action_path), f"Action file not found at {my_action_path}"

    # Load the action.yml file
    with open(my_action_path, 'r') as f:
        action = yaml.safe_load(f)

    # Test the action structure
    # ...
```

## Adding Tests for New Actions

When adding a new action to the repository, you should
also add a corresponding test file in this directory.
The test file should follow the naming convention
`test_<action_name>_action.py` and should test the
specific structure and functionality of the action.
Use the fixtures provided in `conftest.py` to simplify path handling.
