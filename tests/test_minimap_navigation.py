from pathlib import Path

import cv2
import pytest
import pytest_html

from navigation.minimap import LocalNavigator, MinimapAnalyzer, draw_debug
from screenCapture.minimap_carture.minimap_capture import MinimapCapture
from tests.conftest import base_image_array


class TestNavigator:

    @pytest.mark.parametrize('minimap_image, expected_location',
                             [pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                                           (120, 155),
                                           id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"),
                              # TODO: rename
                              ], indirect=['minimap_image'])
    def test_minimap_detects_player_and_water(self, minimap_image, expected_location, extras):
        minimap = MinimapAnalyzer().analyze(MinimapCapture.capture)

        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_player(minimap), mode='RGB')))
        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_water(minimap), mode='RGB')))
        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_road(minimap), mode='RGB')))

        px, py = minimap.player
        # TODO: split
        assert 120 <= px <= 155
        assert 120 <= py <= 155
        assert minimap.water_mask.sum() > 5_000
        assert minimap.road_mask.sum() > 500

    @pytest.mark.parametrize('minimap_image, expected_location',
                             [pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                                           (298515, 221476, 10289, 270, 269),
                                           id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"), ],
                             # TODO: target is not defined
                             indirect=['minimap_image'])
    def test_minimap_finds_water_shore_and_path(self, minimap_image, expected_location, extras):
        minimap = MinimapAnalyzer().analyze(MinimapCapture.capture)
        result = LocalNavigator().find_nearest_water(MinimapCapture.capture)

        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_player(minimap), mode='RGB')))
        extras.append(
            pytest_html.extras.image(base_image_array(MinimapCapture.draw_target(minimap, result), mode='RGB')))
        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_water(minimap), mode='RGB')))
        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_road(minimap), mode='RGB')))

        assert result.target is not None
        assert result.path
        assert result.path[0][0] >= 0
        assert result.path[0][1] >= 0
        assert result.water_mask.sum() > 5_000

    @pytest.mark.parametrize('minimap_image, expected_location',
                             [pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                                           (120, 155),
                                           id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"),
                              # TODO: rename
                              ], indirect=['minimap_image'])
    def test_minimap_debug_image_can_be_saved(self, minimap_image, expected_location, extras):
        minimap = MinimapAnalyzer().analyze(MinimapCapture.capture)
        result = LocalNavigator().find_nearest_water(MinimapCapture.capture)
        debug = draw_debug(minimap, result)

        extras.append(pytest_html.extras.image(base_image_array(debug, mode='RGB')))

        assert debug.size > 0

