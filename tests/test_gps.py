import pytest
from moving.gps import Gps


class TestGPS:
    @pytest.mark.parametrize(
        'current_destination_point, is_it_destination_point', [
            pytest.param((0, 0), True, id="(0, 0) ~ (0, 0)"),
            pytest.param((0.03, 0.03), True, id="(0.03, 0.03) ~ (0, 0)"),
            pytest.param((-0.03, -0.03), True, id="(-0.03, -0.03) ~ (0, 0)"),
            pytest.param((0.04, 0.04), False, id="(0.04, 0.04) !~ (0, 0)"),
            pytest.param((-0.04, -0.04), False, id="(-0.04, -0.04) !~ (0, 0)")])
    def test_is_it_destination_point(self, current_destination_point, is_it_destination_point):
        Gps.current_position = current_destination_point
        Gps.current_destination = (0, 0)
        assert Gps.is_it_destination_point() == is_it_destination_point
