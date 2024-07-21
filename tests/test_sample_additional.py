import pytest
import numpy as np
import torch
from embdata.sample import Sample

def test_flatten_recursive():
    sample = Sample(
        a=1,
        b={
            "c": 2,
            "d": [3, 4]
        },
        e=Sample(
            f=5,
            g={
                "h": 6,
                "i": 7
            }
        )
    )
    flattened = Sample.flatten_recursive(sample.dump())
    expected = [
        ('a', 1),
        ('b.c', 2),
        ('b.d.0', 3),
        ('b.d.1', 4),
        ('e.f', 5),
        ('e.g.h', 6),
        ('e.g.i', 7)
    ]
    assert flattened == expected, f"Expected {expected}, but got {flattened}"

def test_flatten_recursive_with_ignore():
    sample = Sample(
        a=1,
        b={
            "c": 2,
            "d": [3, 4]
        },
        e=Sample(
            f=5,
            g={
                "h": 6,
                "i": 7
            }
        )
    )
    flattened = Sample.flatten_recursive(sample.dump(), ignore={"b"})
    expected = [
        ('a', 1),
        ('e.f', 5),
        ('e.g.h', 6),
        ('e.g.i', 7)
    ]
    assert flattened == expected, f"Expected {expected}, but got {flattened}"

def test_group_values():
    flattened = [
        ('a', 1),
        ('b.c', 2),
        ('b.d.0', 3),
        ('b.d.1', 4),
        ('e.f', 5),
        ('e.g.h', 6),
        ('e.g.i', 7)
    ]
    grouped = Sample.group_values(flattened, ["a", "b.c", "e.g.h"])
    expected = {
        "a": [1],
        "b.c": [2],
        "e.g.h": [6]
    }
    assert grouped == expected, f"Expected {expected}, but got {grouped}"

def test_group_values_with_wildcard():
    flattened = [
        ('a', 1),
        ('b.c', 2),
        ('b.d.0', 3),
        ('b.d.1', 4),
        ('e.f', 5),
        ('e.g.h', 6),
        ('e.g.i', 7)
    ]
    grouped = Sample.group_values(flattened, ["a", "b.*", "e.g.h"])
    expected = {
        "a": [1],
        "b.*": [2, 3, 4],
        "e.g.h": [6]
    }
    assert grouped == expected, f"Expected {expected}, but got {grouped}"

def test_group_values_with_multiple_matches():
    flattened = [
        ('a', 1),
        ('b.c', 2),
        ('b.d', 3),
        ('b.e', 4),
        ('c.d', 5),
        ('c.e', 6)
    ]
    grouped = Sample.group_values(flattened, ["a", "b.*", "c.*"])
    expected = {
        "a": [1],
        "b.*": [2, 3, 4],
        "c.*": [5, 6]
    }
    assert grouped == expected, f"Expected {expected}, but got {grouped}"

def test_flatten_recursive_with_numpy_and_torch():
    sample = Sample(
        a=1,
        b=np.array([2, 3]),
        c=torch.tensor([4, 5]),
        d=Sample(
            e=6,
            f=np.array([7, 8]),
            g=torch.tensor([9, 10])
        )
    )
    flattened = Sample.flatten_recursive(sample.dump())
    expected = [
        ('a', 1),
        ('b.0', 2),
        ('b.1', 3),
        ('c.0', 4),
        ('c.1', 5),
        ('d.e', 6),
        ('d.f.0', 7),
        ('d.f.1', 8),
        ('d.g.0', 9),
        ('d.g.1', 10)
    ]
    assert flattened == expected, f"Expected {expected}, but got {flattened}"

def test_group_values_with_nested_structure():
    flattened = [
        ('a', 1),
        ('b.c', 2),
        ('b.d.0', 3),
        ('b.d.1', 4),
        ('e.f', 5),
        ('e.g.h', 6),
        ('e.g.i', 7),
        ('x.y.z', 8)
    ]
    grouped = Sample.group_values(flattened, ["a", "b.*", "e.g.*", "x.*"])
    expected = {
        "a": [1],
        "b.*": [2, 3, 4],
        "e.g.*": [6, 7],
        "x.*": [8]
    }
    assert grouped == expected, f"Expected {expected}, but got {grouped}"

def test_flatten_recursive_with_list_of_samples():
    sample = Sample(
        a=1,
        b=[
            Sample(c=2, d=3),
            Sample(c=4, d=5)
        ],
        e=Sample(
            f=6,
            g=[
                Sample(h=7, i=8),
                Sample(h=9, i=10)
            ]
        )
    )
    flattened = Sample.flatten_recursive(sample.dump())
    expected = [
        ('a', 1),
        ('b.0.c', 2),
        ('b.0.d', 3),
        ('b.1.c', 4),
        ('b.1.d', 5),
        ('e.f', 6),
        ('e.g.0.h', 7),
        ('e.g.0.i', 8),
        ('e.g.1.h', 9),
        ('e.g.1.i', 10)
    ]
    assert flattened == expected, f"Expected {expected}, but got {flattened}"

def test_group_values_with_complex_wildcards():
    flattened = [
        ('a.b.c', 1),
        ('a.b.d', 2),
        ('a.x.y', 3),
        ('b.c.d', 4),
        ('b.c.e', 5),
        ('b.x.y', 6),
        ('c.d.e', 7)
    ]
    grouped = Sample.group_values(flattened, ["a.b.*", "*.c.*", "c.*"])
    expected = {
        "a.b.*": [1, 2],
        "*.c.*": [1, 2, 4, 5],
        "c.*": [7]
    }
    assert grouped == expected, f"Expected {expected}, but got {grouped}"

if __name__ == "__main__":
    pytest.main()
