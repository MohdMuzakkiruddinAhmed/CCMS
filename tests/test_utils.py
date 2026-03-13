"""Unit tests for CCMS utils module."""
import pytest
from ccms.utils import compute_twi, count_intersections, disaggregate_by_size
from ccms.core import compute_ccms


def test_compute_twi_basic():
    assert compute_twi(4, 9, 6) == pytest.approx(1.0)


def test_compute_twi_zero_intersections():
    assert compute_twi(4, 9, 0) == 0.0


def test_count_intersections():
    er1 = {"1": "a", "2": "a", "3": "b"}
    er2 = {"1": "x", "2": "y", "3": "x"}
    assert count_intersections(er1, er2) == 3


def test_count_intersections_partial_overlap():
    er1 = {"1": "a", "2": "b"}
    er2 = {"1": "x"}  # record 2 missing from er2
    assert count_intersections(er1, er2) == 1


def test_disaggregate_by_size():
    er1 = {"1": "a", "2": "b", "3": "b"}
    er2 = {"1": "x", "2": "y", "3": "y"}
    result = compute_ccms(er1, er2)
    size_table = disaggregate_by_size(result)
    assert 1 in size_table
    assert 2 in size_table
    assert size_table[1]["UC"] == 1
    assert size_table[2]["UC"] == 1
