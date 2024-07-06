# coding=utf-8

from unittest import TestCase

from ctr4ever.services.timeparser import TimeParser


class TimeParserTest(TestCase):

    def setUp(self):
        self.time_parser = TimeParser()

    def test_can_parse_time(self):
        time = self.time_parser.parse_time('1:18.59')

        self.assertEqual(time._minutes, 1)
        self.assertEqual(time._seconds, 18)
        self.assertEqual(time._milliseconds, 59)

    def test_can_not_parse_time(self):
        time = self.time_parser.parse_time('test')
        self.assertIsNone(time)

    def test_can_not_parse_time_when_time_is_not_a_string(self):
        time = self.time_parser.parse_time(12345678)
        self.assertIsNone(time)

    def test_can_convert_time_to_seconds(self):
        time = self.time_parser.parse_time('1:20.39')
        self.assertEqual(time.in_seconds(), 80.39)

    def test_can_convert_time_to_dict(self):
        time = self.time_parser.parse_time('2:57.48')
        data = time.to_dict()

        self.assertEqual(data['minutes'], 2)
        self.assertEqual(data['seconds'], 57)
        self.assertEqual(data['milliseconds'], 48)
