# coding=utf-8

import re
from typing import Optional


class Time(object):

    def __init__(self, minutes: int, seconds: int, milliseconds: int) -> None:
        self._minutes = minutes
        self._seconds = seconds
        self._milliseconds = milliseconds

    def get_minutes(self) -> int:
        return self._minutes

    def get_seconds(self) -> int:
        return self._seconds

    def get_milliseconds(self) -> int:
        return self._milliseconds

    def in_seconds(self) -> float:
        return (self._minutes * 60) + self._seconds + (self._milliseconds / 100)

    def to_dict(self) -> dict[str, int]:
        return {
            'minutes': self._minutes,
            'seconds': self._seconds,
            'milliseconds': self._milliseconds
        }


class TimeParser(object):

    def __init__(self):
        self._regex = r'([0-9]{1})\:([0-5]{1}[0-9]{1})\.([0-9]{2})'

    def parse_time(self, time: str) -> Optional[Time]:
        if not isinstance(time, str):
            return None

        match = re.match(self._regex, time)

        if not match:
            return None

        return Time(int(match.group(1)), int(match.group(2)), int(match.group(3)))
