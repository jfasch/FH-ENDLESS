from endless.framework.component import Component
from endless.framework.facet import facet
from endless.framework.receptacle import receptacle, ONE

import pytest
import abc


def test_connected_components():
    class SimpleCalculator(abc.ABC):
        @abc.abstractmethod
        def add(self, lhs, rhs):
            raise NotImplementedError
        @abc.abstractmethod
        def sub(self, lhs, rhs):
            raise NotImplementedError

    class SuperStatistics(abc.ABC):
        @abc.abstractmethod
        def add(self, value):
            raise NotImplementedError
        @abc.abstractmethod
        def get_accumulated_value(self):
            raise NotImplementedError
        @abc.abstractmethod
        def get_average_value(self):
            raise NotImplementedError

    @facet('calculator', SimpleCalculator,
           (('add', '_add'),    # SimpleCalculator.add -> MyCalculatingThing._add
            ('sub', '_sub'),    # SimpleCalculator.sub -> MyCalculatingThing._sub
            ))  
    @facet('statistics', SuperStatistics, 
           (('add', '_present_value'),                      # SuperStatistics.add -> MyCalculatingThing._present_value
            ('get_accumulated_value', '_get_accumulated'),  # SuperStatistics.get_accumulated_value -> MyCalculatingThing._get_accumulated
            ('get_average_value', '_get_running_average'),  # SuperStatistics.get_average_value -> MyCalculatingThing._get_running_average
            ))
    class MyCalculatingThing(Component):
        def __init__(self):
            super().__init__()
            self._accumulated_value = 0
            self._running_average = 0
            self._nvalues = 0

        def _add(self, lhs, rhs):
            return lhs + rhs
        def _sub(self, lhs, rhs):
            return lhs - rhs

        def _present_value(self, value):
            self._accumulated_value += value
            if self._nvalues == 0:
                self._running_average = value
            else:
                self._running_average = (self._running_average * self._nvalues + value) / (self._nvalues + 1)
            self._nvalues += 1

        def _get_accumulated(self):
            return self._accumulated_value
        def _get_running_average(self):
            return self._running_average

    @receptacle('statistical_outlet', SuperStatistics, multiplicity=ONE)
    class ValueProducer(Component):
        '''Produces values from an iterable, and injects it into
        another component that is connected via the
        ``statistical_outlet`` receptacle'''

        def __init__(self, values):
            super().__init__()
            self._iter = iter(values)
        def produce_next_value(self):
            '''Produce next value, and inject it into receptacle'''
            self._statistical_outlet.add(next(self._iter))

    my_values = ValueProducer([1,5,3,4])
    my_calc_thing = MyCalculatingThing()

    # connect both together (using only statistics functionality,
    # disregarding calculator)

    my_values.statistical_outlet.connect(my_calc_thing.statistics)

    # component "pipeline": produce values, and check flow into
    # statistics
    my_values.produce_next_value()      # <-- 1
    assert my_calc_thing.statistics.get_accumulated_value() == 1
    assert my_calc_thing.statistics.get_average_value() == 1

    my_values.produce_next_value()      # <-- 5
    assert my_calc_thing.statistics.get_accumulated_value() == 6
    assert my_calc_thing.statistics.get_average_value() == pytest.approx(3)

    my_values.produce_next_value()      # <-- 3
    assert my_calc_thing.statistics.get_accumulated_value() == 9
    assert my_calc_thing.statistics.get_average_value() == pytest.approx(3)

    my_values.produce_next_value()      # <-- 4
    assert my_calc_thing.statistics.get_accumulated_value() == 13
    assert my_calc_thing.statistics.get_average_value() == pytest.approx(3.25)

    # use calculator facet directly
    sum = my_calc_thing.calculator.add(1, 2)
    diff = my_calc_thing.calculator.sub(1, 2)

    assert sum == 3
    assert diff == -1
            
