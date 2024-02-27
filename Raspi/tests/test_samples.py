from endless.sample import Sample

import pytest


def test_basic():
    sample = Sample('name', 100, 42.666)
    assert sample.name == 'name'
    assert sample.timestamp_ms == 100
    assert sample.temperature == pytest.approx(42.666)

    sample = Sample(name='name', timestamp_ms=100, temperature=42.666)
    assert sample.name == 'name'
    assert sample.timestamp_ms == 100
    assert sample.temperature == pytest.approx(42.666)

def test_frozen():
    sample = Sample('name', 100, 42.666)
    with pytest.raises(Exception):
        sample.name = 'another-name'
    with pytest.raises(Exception):
        sample.timestamp_ms = 200
    with pytest.raises(Exception):
        sample.name = 'another-name'
