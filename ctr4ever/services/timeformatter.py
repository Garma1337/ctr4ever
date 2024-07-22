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


class TimeFormatter(object):

    def parse_time(self, time: float):
        if not isinstance(time, float):
            return None

        minutes = int(time / 60)
        seconds = int(time % 60)
        milliseconds = int(round((time % 1) * 100))

        return Time(minutes, seconds, milliseconds)

    def create_time_from_format(self, time: str) -> Optional[Time]:
        if not isinstance(time, str):
            return None

        matches = re.match(r'([0-9]:)?([0-5][0-9])\.([0-9]{2})', time)

        if not matches:
            return None

        minutes = matches.group(1)

        if minutes:
            minutes = int(minutes.replace(':', ''))
        else:
            minutes = 0

        seconds = int(matches.group(2))
        milliseconds = int(matches.group(3))

        return Time(minutes, seconds, milliseconds)

    def format_time(self, time: Time):
        if time.get_minutes() <= 0:
            return f'{time.get_seconds():02}.{time.get_milliseconds():02}'

        return f'{time.get_minutes()}:{time.get_seconds():02}.{time.get_milliseconds():02}'
