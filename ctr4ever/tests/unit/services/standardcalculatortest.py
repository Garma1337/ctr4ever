# coding=utf-8

from unittest import TestCase

from ctr4ever.services.standardcalculator import StandardCalculator, StandardCalculatorError
from ctr4ever.services.timeformatter import TimeFormatter
from ctr4ever.tests.mockmodelrepository import MockStandardTimeRepository


class StandardCalculatorTest(TestCase):

    def setUp(self):
        self.time_formatter = TimeFormatter()
        self.standard_time_repository = MockStandardTimeRepository()

        self.standard_time_repository.create(1, 1, 1, 79.50, 0)
        self.standard_time_repository.create(1, 1, 1, 79.75, 1)
        self.standard_time_repository.create(1, 1, 1, 80, 2)

        self.standard_calculator = StandardCalculator(
            self.time_formatter,
            self.standard_time_repository
        )

    def test_can_calculate_standard(self):
        standard_time = self.standard_calculator.calculate_standard(1, 1, 1, 79.39)
        self.assertEqual(standard_time.id, 1)

    def test_can_not_calculate_standard_when_no_standards_exist(self):
        self.standard_calculator._standard_times = []
        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 1, 1, 78.59)

    def test_can_not_calculate_standard_when_no_standards_exist_for_standard_set(self):
        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 2, 1, 1, 80.31)

    def test_can_not_calculate_standard_when_no_standards_exist_for_track(self):
        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 2, 1, 80.31)

    def test_can_not_calculate_standard_when_no_standards_exist_for_category(self):
        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 1, 2, 80.31)

    def test_can_not_calculate_standard_when_no_suitable_standard_exists(self):
        self.assertRaises(StandardCalculatorError, self.standard_calculator.calculate_standard, 1, 1, 1, 80.31)

    def test_can_order_standards_by_numeric_value(self):
        standard_times = self.standard_calculator._find_standard_times(1, 1, 1)

        self.assertEqual(standard_times[0].numeric_value, 0)
        self.assertEqual(standard_times[1].numeric_value, 1)
        self.assertEqual(standard_times[2].numeric_value, 2)
