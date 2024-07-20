# coding=utf-8

from unittest import TestCase

from ctr4ever.services.timeformatter import TimeFormatter


class TimeFormatterTest(TestCase):

    def setUp(self):
        self.time_formatter = TimeFormatter()

    def test_can_parse_time(self):
        time = self.time_formatter.parse_time(78.53)

        self.assertEqual(time._minutes, 1)
        self.assertEqual(time._seconds, 18)
        self.assertEqual(time._milliseconds, 53)

    def test_can_not_parse_time_when_time_is_not_a_number(self):
        time = self.time_formatter.parse_time('test')
        self.assertIsNone(time)

    def test_can_format_time_with_minutes(self):
        time = self.time_formatter.parse_time(78.53)
        self.assertEqual(self.time_formatter.format_time(time), '1:18.53')

    def test_can_format_time_without_minutes(self):
        time = self.time_formatter.parse_time(41.41)
        self.assertEqual(self.time_formatter.format_time(time), '41.41')

    def test_can_convert_time_to_dict(self):
        time = self.time_formatter.parse_time(177.48)
        data = time.to_dict()

        self.assertEqual(data['minutes'], 2)
        self.assertEqual(data['seconds'], 57)
        self.assertEqual(data['milliseconds'], 48)
