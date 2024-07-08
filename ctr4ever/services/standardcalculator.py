# coding=utf-8

from typing import List

from ctr4ever.models.repository.standardtimerepository import StandardTimeRepository
from ctr4ever.models.standardtime import StandardTime
from ctr4ever.services.timeformatter import TimeFormatter


class StandardCalculatorError(Exception):
    pass


class StandardCalculator(object):

    def __init__(self, time_formatter: TimeFormatter, standard_time_repository: StandardTimeRepository):
        self.time_formatter: TimeFormatter = time_formatter
        self.standard_time_repository = standard_time_repository

        self.standard_times: List[StandardTime] = self.standard_time_repository.find_by()

    def calculate_standard(self, standard_id: int, track_id: int, category_id: int, player_time: float) -> StandardTime:
        standard_times = self._find_standard_times(standard_id, track_id, category_id)

        if len(standard_times) <= 0:
            raise StandardCalculatorError(f'No standard time found in standard set {standard_id} for track {track_id} and category {category_id}')

        standard_time = None

        for time in standard_times:
            if player_time < time.time:
                standard_time = time
                break

        if not standard_time:
            raise StandardCalculatorError(f'No suitable standard found for a time of {player_time} in standard set {standard_id} on track {track_id} in category {category_id}')

        return standard_time

    def _find_standard_times(self, standard_id: int, track_id: int, category_id: int) -> List[StandardTime]:
        standard_times = list(filter(lambda t: t.standard_id == standard_id and t.track_id == track_id and t.category_id == category_id, self.standard_times))
        standard_times = sorted(self.standard_times, key=lambda t: t.numeric_value)

        return standard_times
