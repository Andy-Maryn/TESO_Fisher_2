import pytest

from moving.rotation.rotation import Rotation


class TestRotation:
    @pytest.mark.parametrize(
        'actual_degree, expected_degree', [
            pytest.param(-1, 359, id="-1 => 359"),
            pytest.param(0, 360, id="0 => 360"),
            pytest.param(1, 1, id="1 => 1"),
            pytest.param(359, 359, id="359 => 359"),
            pytest.param(360, 360, id="360 => 360"),
            pytest.param(361, 1, id="361 => 1")])
    def test_degree(self, actual_degree: int, expected_degree):
        assert round(Rotation.degree(actual_degree), 5) == expected_degree

    @pytest.mark.parametrize(
        'start_point, destination_point, expected_degree', [
            pytest.param((0, 0), (9, -3), 341.565, id="x=9,y =-3 => 341.565"),
            pytest.param((0, 0), (9, 0), 360, id="x=9,y =0 => 360"),
            pytest.param((0, 0), (9, 3), 18.435, id="x=9,y =3 => 18.435"),

            pytest.param((0, 0), (-3, 9), 108.435, id="x=-3,y =9 => 108.435"),
            pytest.param((0, 0), (0, 9), 90, id="x=0,y =9 => 90"),
            pytest.param((0, 0), (3, 9), 71.565, id="x=3,y =9 => 71.565"),

            pytest.param((0, 0), (-9, -3), 198.435, id="x=-9,y =-3 => 198.435"),
            pytest.param((0, 0), (-9, 0), 180, id="x=-9,y =0 => 180"),
            pytest.param((0, 0), (-9, 3), 161.565, id="x=-9,y =3 => 161.565"),

            pytest.param((0, 0), (-3, -9), 251.565, id="x=-3,y =-9 => 251.565"),
            pytest.param((0, 0), (0, -9), 270, id="x=0,y =-9 => 270"),
            pytest.param((0, 0), (3, -9), 288.435, id="x=3,y =-9 => 288.435"),
        ])
    def test_get_degree_between_2_points(self,
                                         start_point: tuple[float, float],
                                         destination_point: tuple[float, float],
                                         expected_degree: float):
        actual_degree = round(Rotation.get_degree_between_2_points(start_point, destination_point), 3)
        assert actual_degree == expected_degree
