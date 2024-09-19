from fisherman.fisherman import Fisherman
from tests.common import *
from tests.conftest import TESO_RUNNING


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
            pytest.param((0, 0), (6, -3), 333.435, id="x=6,y =-3 => 333.435"),
            pytest.param((0, 0), (6, 0), 360, id="x=6,y =0 => 360"),
            pytest.param((0, 0), (6, 3), 26.565, id="x=6,y =3 => 26.565"),

            pytest.param((0, 0), (-3, 6), 116.565, id="x=-3,y =6 => 116.565"),
            pytest.param((0, 0), (0, 6), 90, id="x=0,y =6 => 90"),
            pytest.param((0, 0), (3, 6), 63.435, id="x=3,y =6 => 63.435"),

            pytest.param((0, 0), (-6, -3), 206.565, id="x=-6,y =-3 => 206.565"),
            pytest.param((0, 0), (-6, 0), 180, id="x=-6,y =0 => 180"),
            pytest.param((0, 0), (-6, 3), 153.435, id="x=-6,y =3 => 153.435"),

            pytest.param((0, 0), (-3, -6), 243.435, id="x=-3,y =-6 => 243.435"),
            pytest.param((0, 0), (0, -6), 270, id="x=0,y =-6 => 270"),
            pytest.param((0, 0), (3, -6), 296.565, id="x=3,y =-6 => 296.565"),
        ])
    def test_get_degree(self,
                        start_point: tuple[float, float],
                        destination_point: tuple[float, float],
                        expected_degree: float):
        actual_degree = round(Rotation.get_degree(start_point, destination_point), 3)
        assert actual_degree == expected_degree

    @pytest.mark.parametrize(
        'degree, compas_degree, expected_degree', [
            pytest.param(75, 0, -75, id="75 / 0 => degree: -75"),
            pytest.param(75, 90, 15, id="75 / 90 => degree: 15"),
            pytest.param(75, 180, 105, id="75 / 180 => degree: 105"),
            pytest.param(75, 270, -165, id="75 / 270 => degree: -165"),
            pytest.param(75, 360, -75, id="75 / 360 => degree: -75"),
            pytest.param(75, 75, 0, id="75 / 75 => degree: 0"),
            pytest.param(75, 255, 180, id="75 / 255 => degree: 180"),
        ])
    def test_calibration(self,
                         degree: tuple[float, float],
                         compas_degree: float,
                         expected_degree: float):
        assert round(Rotation._calibrate(degree, compas_degree)) == expected_degree

    @pytest.mark.parametrize(
        'move', [
            pytest.param(10, id="10=> calibration"),
            pytest.param(-10, id="-10 => calibration"),
            pytest.param(15, id="15 => calibration"),
            pytest.param(-15, id="-15 => calibration"),
            pytest.param(20, id="20 => calibration"),
            pytest.param(-20, id="-20 => calibration"),
            pytest.param(25, id="25 => calibration"),
            pytest.param(-25, id="-25 => calibration"),
            pytest.param(30, id="30 => calibration"),
            pytest.param(-30, id="-30 => calibration"),
            pytest.param(35, id="35 => calibration"),
            pytest.param(-35, id="-35 => calibration"),
            pytest.param(40, id="40 => calibration"),
            pytest.param(-40, id="-40 => calibration"),
        ])
    @pytest.mark.skipif(TESO_RUNNING is not True, reason="'eso64.exe' is not running")
    def test_calibration_runtime(self, move, load_data, screen_is_ready, mouse_sensitivity):
        Rotation.move_mouse(move)

        Fisherman.set_current_position()
        logger.info(f"-current_position: {Gps.current_position}")

        Fisherman.set_destination_point()
        logger.info(f"-destination_point: {Gps.current_destination}")

        calibration =Fisherman.direction_of_view()
        logger.info(f"-calibration: {calibration}")

        assert -3 < calibration < 3
