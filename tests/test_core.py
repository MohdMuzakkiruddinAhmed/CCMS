"""Unit tests for CCMS core module."""
import pytest
from ccms.core import compute_ccms


@pytest.fixture
def example_16ref():
    """16-reference example from the paper."""
    er1 = {
        "1": "a", "2": "b", "3": "b",
        "4": "c", "5": "c", "6": "c",
        "7": "d",
        "8": "e", "9": "e", "10": "e",
        "11": "f", "12": "f", "13": "f",
        "14": "g", "15": "g", "16": "g",
    }
    er2 = {
        "1": "x", "2": "y", "3": "y",
        "4": "z", "5": "z", "6": "z", "7": "z",
        "8": "w", "9": "w", "10": "t",
        "11": "u", "12": "u", "13": "v",
        "14": "u", "15": "v", "16": "s",
    }
    return er1, er2


def test_case_counts(example_16ref):
    er1, er2 = example_16ref
    result = compute_ccms(er1, er2)
    assert result["UC"] == 2
    assert result["MC"] == 2
    assert result["PC"] == 1
    assert result["OC"] == 2


def test_cluster_counts(example_16ref):
    er1, er2 = example_16ref
    result = compute_ccms(er1, er2)
    assert result["CC1"] == 7
    assert result["CC2"] == 8


def test_singleton_counts(example_16ref):
    er1, er2 = example_16ref
    result = compute_ccms(er1, er2)
    assert result["SC1"] == 2
    assert result["SC2"] == 3


def test_sum_property(example_16ref):
    """UC + MC + PC + OC must equal CC1."""
    er1, er2 = example_16ref
    result = compute_ccms(er1, er2)
    total = result["UC"] + result["MC"] + result["PC"] + result["OC"]
    assert total == result["CC1"]


def test_identical_clusterings():
    """Two identical clusterings should produce all Unchanged."""
    er = {"1": "a", "2": "a", "3": "b", "4": "c"}
    result = compute_ccms(er, er)
    assert result["UC"] == 3
    assert result["MC"] == 0
    assert result["PC"] == 0
    assert result["OC"] == 0


def test_all_merged():
    """All records in one ER2 cluster."""
    er1 = {"1": "a", "2": "b", "3": "c"}
    er2 = {"1": "x", "2": "x", "3": "x"}
    result = compute_ccms(er1, er2)
    assert result["MC"] == 3
    assert result["UC"] == 0


def test_all_partitioned():
    """Each ER1 cluster split into singletons in ER2."""
    er1 = {"1": "a", "2": "a", "3": "b", "4": "b"}
    er2 = {"1": "w", "2": "x", "3": "y", "4": "z"}
    result = compute_ccms(er1, er2)
    assert result["PC"] == 2
    assert result["UC"] == 0
    assert result["MC"] == 0
    assert result["OC"] == 0
