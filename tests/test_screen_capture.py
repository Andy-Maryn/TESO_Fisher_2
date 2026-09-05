from pathlib import Path

import pytest
import pytest_html

from screenCapture.coords_and_heading_capture.coords_and_heading_capture import CoordsAndHeadingCapture
from tests.conftest import base_image_array


class TestCoordsAndHeadingCapture:
    @pytest.mark.requirement("FRS_TESO_FISHER_010103")
    @pytest.mark.parametrize(
        'eso_locate_capture, expected_location', [
            pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                         (298515, 221476, 10289, 270, 269),
                         id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"),
        ], indirect=['eso_locate_capture']
    )
    def test_get_current_coordinates(self,
                                     eso_locate_capture: Path,
                                     expected_location: tuple[float, float],
                                     load_test_data,
                                     extras):
        extras.append(
            pytest_html.extras.image(
                base_image_array(CoordsAndHeadingCapture.capture, mode='1')
            )
        )
        coords_and_heading = CoordsAndHeadingCapture.get_numbers()
        actual_position = (
            coords_and_heading.x,
            coords_and_heading.y,
            coords_and_heading.z,
            coords_and_heading.char_heading,
            coords_and_heading.camera_heading,
        )
        assert actual_position == expected_location
