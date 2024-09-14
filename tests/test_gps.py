import pytest

from moving.gps import Gps


class TestGPS:
    @pytest.mark.parametrize(
        'current_destination_point, is_it_destination_point', [
            pytest.param((0, 0), True, id="(40.07, 84.28) ~  => (40.07, 84.28)"),
            pytest.param((0.3, 0.3), True, id="(40.74, 81.7) ~  => (40.74, 81.7)"),
            pytest.param((-0.3, -0.3), True, id="(40.74, 81.7) ~  => (40.74, 81.7)"),
            pytest.param((0.4, 0.4), False, id="(40.74, 81.7) ~  => (40.74, 81.7)"),
            pytest.param((-0.4, -0.4), False, id="(40.74, 81.7) ~  => (40.74, 81.7)")])
    def test_is_it_destination_point(self, current_destination_point, is_it_destination_point):
        Gps.current_position = current_destination_point
        Gps.current_destination = (0, 0)
        assert Gps.is_it_destination_point() == is_it_destination_point