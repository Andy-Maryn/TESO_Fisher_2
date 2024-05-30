import time

import pytest

from tests.common import *


class TestESOLocateCapture:
    @pytest.mark.skip
    @pytest.mark.parametrize(
        'eso_locate_capture, expected_location', [
            pytest.param(Path("4715_8270.jpeg"), [47.15, 82.70], id="4715_8270.jpeg => position: [47.15, 82.70]"),
            pytest.param(Path("4719_8287.jpeg"), [47.19, 82.87], id="4719_8287.jpeg => position: [[47.19, 82.87]"),
        ], indirect=['eso_locate_capture']
    )
    def test_get_current_position(self,
                                  eso_locate_capture: None,
                                  expected_location: tuple[float, float]):
        actual_position = ESOLocateCapture.get_current_position()
        assert actual_position == expected_location


class TestYetAnotherCompassCapture:
    @pytest.mark.skip
    @pytest.mark.parametrize(
        'yet_another_compass_capture, expected_location', [
            pytest.param(Path("4730_8228.jpeg"), (-21, 55), id="4730_8228.jpeg => tip: (-21, 55)"),
            pytest.param(Path("4739_8325.jpeg"), (32, 39), id="4739_8325.jpeg => tip: (32, 39)"),
            pytest.param(Path("4777_8315.jpeg"), (49, -18), id="4777_8315.jpeg => tip: (49, -18)"),
        ], indirect=['yet_another_compass_capture'])
    def test_get_compas_direction(self,
                                  yet_another_compass_capture: None,
                                  expected_location: tuple[float, float]):
        actual_position = YetAnotherCompassCapture.get_compas_direction()
        assert actual_position == expected_location

    @pytest.mark.skip
    def test_get_compas_direction_(self, load_data):
        time.sleep(3)
        YetAnotherCompassCapture.get_cap()

        current_time = time.time()
        folder = time.strftime(f"%Y%m%d_%H%M%S_{round(current_time * 1000)}", time.gmtime(current_time))
        os.makedirs(f"report/{folder}")

        Image.fromarray(YetAnotherCompassCapture.start_capture).save(os.path.dirname(os.path.abspath(__file__)) + f"/report/{folder}/compas.jpeg")

