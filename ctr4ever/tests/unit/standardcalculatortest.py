# coding=utf-8

from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from ctr4ever.models.standardtime import StandardTime
from ctr4ever.services.standardcalculator import StandardCalculator, StandardCalculatorError
from ctr4ever.services.timeformatter import TimeFormatter


class StandardCalculatorTest(TestCase):

    def setUp(self):
        self._set_up([])

    def _set_up(self, standard_times: List[StandardTime] = None):
        self.time_formatter = TimeFormatter()

        self.standard_time_repository = MagicMock()
        self.standard_time_repository.find_by = MagicMock(return_value=standard_times)

        self.standard_calculator = StandardCalculator(
            self.time_formatter,
            self.standard_time_repository
        )

    def test_can_calculate_standard(self):
        self._set_up([
            StandardTime(id=1, standard_id=1, track_id=1, category_id=1, time=79.50, numeric_value=0, name='God'),
            StandardTime(id=2, standard_id=1, track_id=1, category_id=1, time=79.75, numeric_value=1, name='Titan A')
        ])

        standard_time = self.standard_calculator.calculate_standard(1, 1, 1, 79.39)
        self.assertEqual(standard_time.name, 'God')

    def test_can_not_calculate_standard_when_no_standards_exist(self):
        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 1, 1, 78.59)

    def test_can_not_calculate_standard_when_no_standards_exist_for_standard_set(self):
        self._set_up([
            StandardTime(id=1, standard_id=2, track_id=1, category_id=1, time=79.50, numeric_value=0, name='God'),
        ])

        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 2, 1, 1, 80.31)

    def test_can_not_calculate_standard_when_no_standards_exist_for_track(self):
        self._set_up([
            StandardTime(id=1, standard_id=1, track_id=1, category_id=1, time=79.50, numeric_value=0, name='God'),
        ])

        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 2, 1, 80.31)

    def test_can_not_calculate_standard_when_no_standards_exist_for_category(self):
        self._set_up([
            StandardTime(id=1, standard_id=1, track_id=1, category_id=2, time=79.50, numeric_value=0, name='God'),
        ])

        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 1, 2, 80.31)

    def test_can_not_calculate_standard_when_no_suitable_standard_exists(self):
        self._set_up([StandardTime(id=1, standard_id=1, track_id=1, category_id=1, time=79.50, numeric_value=0, name='God')])
        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 1, 1, 80.31)

    def test_can_order_standards_by_numeric_value(self):
        self._set_up([
            StandardTime(id=1, standard_id=1, track_id=1, category_id=1, time=80, numeric_value=2, name='Titan B'),
            StandardTime(id=2, standard_id=1, track_id=1, category_id=1, time=79.75, numeric_value=1, name='Titan A'),
            StandardTime(id=3, standard_id=1, track_id=1, category_id=1, time=79.50, numeric_value=0, name='God'),
        ])

        standard_times = self.standard_calculator._find_standard_times(1, 1, 1)

        self.assertEqual(standard_times[0].numeric_value, 0)
        self.assertEqual(standard_times[1].numeric_value, 1)
        self.assertEqual(standard_times[2].numeric_value, 2)
