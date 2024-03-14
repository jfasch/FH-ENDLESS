from endless.sample import Sample

from datetime import datetime
import pytest


def test_basic():
    sample = Sample('name', datetime(2024, 3, 14, 8, 46), 42.666)
    assert sample.name == 'name'
    assert sample.timestamp == datetime(2024, 3, 14, 8, 46)
    assert sample.temperature == pytest.approx(42.666)

    sample = Sample(name='name', timestamp=datetime(2024, 3, 14, 8, 47), temperature=42.666)
    assert sample.name == 'name'
    assert sample.timestamp == datetime(2024, 3, 14, 8, 47)
    assert sample.temperature == pytest.approx(42.666)

def test_frozen():
    sample = Sample('name', datetime(2024, 3, 14, 8, 46), 42.666)
    with pytest.raises(Exception):
        sample.name = 'another-name'
    with pytest.raises(Exception):
        sample.timestamp = datetime(2024, 3, 14, 8, 47)
    with pytest.raises(Exception):
        sample.name = 'another-name'

def test_check_timestamp_type():
    with pytest.raises(RuntimeError):
        Sample('name', 100, 42.666)

def test_equality():
    sample = Sample('name', datetime(2024, 3, 14, 8, 46), 42.666)

    assert sample == Sample('name', datetime(2024, 3, 14, 8, 46), pytest.approx(42.666))
    assert sample != Sample('name1', datetime(2024, 3, 14, 8, 46), pytest.approx(42.666))
    assert sample != Sample('name', datetime(2024, 2, 14, 8, 46), pytest.approx(42.666))
    assert sample != Sample('name', datetime(2024, 3, 14, 8, 46), pytest.approx(0))
