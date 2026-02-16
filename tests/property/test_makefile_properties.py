"""Property-based tests using Hypothesis.

This module currently exercises generic Python behavior (for example, list sorting)
rather than any project Makefile targets or operations.

Uses Hypothesis to generate test cases that verify behavior across a wide range of inputs.
"""

from __future__ import annotations

import itertools
from collections import Counter

import pytest
from hypothesis import given
from hypothesis import strategies as st


@pytest.mark.property
@given(st.lists(st.integers() | st.floats(allow_nan=False, allow_infinity=False)))
def test_sort_correctness_using_properties(lst):
    """Verify that sorted() correctly orders lists and preserves all elements."""
    result = sorted(lst)
    # Use Counter to ensure multiplicities (duplicates) are preserved
    assert Counter(lst) == Counter(result)
    assert all(a <= b for a, b in itertools.pairwise(result))
