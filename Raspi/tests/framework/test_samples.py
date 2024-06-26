from endless.framework.sample import Sample

from datetime import datetime
import pytest


def test_basic():
    sample = Sample('name', datetime(2024, 3, 14, 8, 46), 42.666)
    assert sample.tag == 'name'
    assert sample.timestamp == datetime(2024, 3, 14, 8, 46)
    assert sample.data == pytest.approx(42.666)

    sample = Sample(tag='name', timestamp=datetime(2024, 3, 14, 8, 47), data=42.666)
    assert sample.tag == 'name'
    assert sample.timestamp == datetime(2024, 3, 14, 8, 47)
    assert sample.data == pytest.approx(42.666)

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
