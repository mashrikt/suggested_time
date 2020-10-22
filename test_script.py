import pytest

from script import suggested_time


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

    def test_sample(self, parameters):
        assert suggested_time(**parameters) == []
