import pytest

from .script import suggested_time


class TestSuggestedTime:

    @pytest.fixture
    def parameters(self):
        return {
            "list_1": ["12:00-12:30", "14:00-15:00"],
            "list_2": ["09:00-12:00", "14:00-15:30"],
            "start_time": "08:00",
            "end_time": "17:00",
            "duration": 60,
        }

    def test_empty_schedule(self, parameters):
        parameters["list_1"] = []
        parameters["list_2"] = []
        result = ["08:00-17:00"]
        assert suggested_time(**parameters) == result

    def test_one_user_single_meeting(self, parameters):
        parameters["list_1"] = ["14:00-15:00"]
        parameters["list_2"] = []
        result = ["08:00-14:00", "15:00-17:00"]
        assert suggested_time(**parameters) == result

    def test_both_user_same_meeting(self, parameters):
        parameters["list_1"] = ["14:00-15:00"]
        parameters["list_2"] = ["14:00-15:00"]
        result = ["08:00-14:00", "15:00-17:00"]
        assert suggested_time(**parameters) == result

    def test_one_user_multiple_meetings(self, parameters):
        parameters["list_1"] = ["14:00-15:00", "16:00-17:00"]
        parameters["list_2"] = []
        result = ["08:00-14:00", "15:00-16:00"]
        assert suggested_time(**parameters) == result

    def test_both_user_multiple_meetings(self, parameters):
        parameters["list_1"] = ["10:30-11:30", "14:00-15:00"]
        parameters["list_2"] = ["09:00-11:00", "15:30-16:00"]
        result = ["08:00-09:00", "11:30-14:00", "16:00-17:00"]
        assert suggested_time(**parameters) == result

    def test_meeting_at_start_of_day(self, parameters):
        parameters["list_1"] = ["05:00-09:30"]
        parameters["list_2"] = []
        result = ["09:30-17:00"]
        assert suggested_time(**parameters) == result

    def test_meeting_at_end_of_day(self, parameters):
        parameters["list_1"] = ["14:00-19:00"]
        parameters["list_2"] = []
        result = ["08:00-14:00"]
        assert suggested_time(**parameters) == result

    @pytest.mark.parametrize(
        "duration,result",
        [
            (5, ["08:00-09:00", "10:00-10:05", "11:00-17:00"]),
            (15, ["08:00-09:00", "11:00-17:00"]),
            (60, ["08:00-09:00", "11:00-17:00"]),
        ]
    )
    def test_smaller_duration_gaps(self, parameters, duration, result):
        parameters["list_1"] = ["9:00-10:00"]
        parameters["list_2"] = ["10:05-11:00"]
        parameters["duration"] = duration
        assert suggested_time(**parameters) == result

    @pytest.mark.parametrize(
        "start_time,end_time,result",
        [
            ("09:00", "19:00", ["12:30-14:00", "15:30-19:00"]),
            ("08:00", "23:59", ["08:00-09:00", "12:30-14:00", "15:30-23:59"]),
            ("00:00", "23:59", ["00:00-09:00", "12:30-14:00", "15:30-23:59"]),
        ]
    )
    def test_varying_start_end_time(self, parameters, start_time, end_time, result):
        parameters["start_time"] = start_time
        parameters["end_time"] = end_time
        assert suggested_time(**parameters) == result
