from tests.common import *
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
        assert round(Rotation._degree(actual_degree), 5) == expected_degree

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
    def test_get_degree(self,
                        start_point: tuple[float, float],
                        destination_point: tuple[float, float],
                        expected_degree: float):
        actual_degree = round(Rotation.get_degree(start_point, destination_point), 3)
        assert actual_degree == expected_degree

    @pytest.mark.parametrize(
        'yet_another_compass_capture, second_point_degree, expected_degree', [
            pytest.param(Path("4730_8228.jpeg"), 110, 1, id="4730_8228.jpeg / 110 => degree: 1"),
            pytest.param(Path("4730_8228.jpeg"), 111, 0, id="4730_8228.jpeg / 111 => tip: 0"),
            pytest.param(Path("4730_8228.jpeg"), 112, -1, id="4730_8228.jpeg / 112 => tip: -1"),
            pytest.param(Path("4730_8228.jpeg"), 290, -179, id="4730_8228.jpeg / 110 => degree: -179"),
            pytest.param(Path("4730_8228.jpeg"), 291, 180, id="4730_8228.jpeg / 291 => degree: 180"),
            pytest.param(Path("4730_8228.jpeg"), 292, 179, id="4730_8228.jpeg / 292 => degree: 179"),
        ], indirect=['yet_another_compass_capture'])
    def test_calibration(self,
                         yet_another_compass_capture: None,
                         second_point_degree: float,
                         expected_degree: float):
        assert round(Rotation.calibration(second_point_degree)) == expected_degree
