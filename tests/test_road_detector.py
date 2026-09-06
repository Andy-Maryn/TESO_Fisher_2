from pathlib import Path

import pytest
import pytest_html

from navigation.minimap.minimap import MinimapAnalyzer
from navigation.road_detector.road_detector import RoadDetector, draw_debug
from screenCapture.minimap_carture.minimap_capture import MinimapCapture
from tests.conftest import base_image_array


class TestRoadDetector:

    @pytest.mark.parametrize('minimap_image, expected_location',
                             [pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                                           (120, 155),
                                           id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"),
                              # TODO: rename
                              ], indirect=['minimap_image'])
    def test_detector(self, minimap_image, expected_location, extras):
        minimap = MinimapAnalyzer().analyze(MinimapCapture.capture)

        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_road(minimap), mode='RGB')))

        d = RoadDetector().detect(minimap.image, minimap.player)

        extras.append(
            pytest_html.extras.image(base_image_array(draw_debug(minimap.image, d, minimap.player), mode='RGB')))

        assert d.candidates.any()
        assert d.road_mask.any()
        print(f"\nCandidates: {(d.candidates > 0).sum()}")
        print(f"Road pixels: {(d.road_mask > 0).sum()}")
        print(f"Best angle: {d.best_angle}")
