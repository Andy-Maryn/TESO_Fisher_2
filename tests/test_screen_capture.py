import time

import pytest
import pytest_html

from tests.common import *
from tests.conftest import base_image_array


class TestESOLocateCapture:
    # @pytest.mark.skip
    @pytest.mark.parametrize(
        'eso_locate_capture, expected_location', [
            pytest.param(Path("4665_7969.jpeg"), [46.65, 79.69], id="4665_7969.jpeg => position: [46.65, 79.69]"),
            pytest.param(Path("4673_8010.jpeg"), [46.73, 80.10], id="4673_8010.jpeg => position: [46.83, 80.10]"),
            pytest.param(Path("4669_7987.jpeg"), [46.69, 79.87], id="4669_7987.jpeg => position: [56.69, 79.87]"),
            pytest.param(Path("4702_8082.jpeg"), [47.02, 80.82], id="4702_8082.jpeg => position: [47.02, 80.82]]"),
        ], indirect=['eso_locate_capture']
    )
    def test_get_current_position(self,
                                  eso_locate_capture: Path,
                                  expected_location: tuple[float, float],
                                  load_test_data,
                                  extras):
        extras.append(
            pytest_html.extras.image(
                base_image_array(ESOLocateCapture.capture, mode='1')
            )
        )
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
