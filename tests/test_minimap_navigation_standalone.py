"""Small standalone regression tests for the minimap CV pipeline."""
from pathlib import Path

import pytest
import pytest_html

from navigation.minimap.minimap import MinimapAnalyzer, LocalNavigator
from screenCapture.minimap_carture.minimap_capture import MinimapCapture
from tests.conftest import base_image_array


class TestNavigatorStandalone:

    @pytest.mark.parametrize('minimap_image, expected_location',
                             [pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                                           (120, 155),
                                           id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"),
                              # TODO: rename
                              ], indirect=['minimap_image'])
    def test_detects_large_water_area(self, minimap_image, expected_location, extras):
        minimap = MinimapAnalyzer().analyze(MinimapCapture.capture)
        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_water(minimap), mode='RGB')))
        assert minimap.water_mask.sum() > 5_000

    @pytest.mark.parametrize('minimap_image, expected_location',
                             [pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                                           (120, 155),
                                           id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"),
                              # TODO: rename
                              ], indirect=['minimap_image'])
    def test_detects_player_near_minimap_center(self, minimap_image, expected_location, extras):
        minimap = MinimapAnalyzer().analyze(MinimapCapture.capture)
        extras.append(pytest_html.extras.image(base_image_array(MinimapCapture.draw_player(minimap), mode='RGB')))
        assert 120 <= minimap.player[0] <= 155
        assert 120 <= minimap.player[1] <= 155

    @pytest.mark.parametrize('minimap_image, expected_location',
                             [pytest.param(Path("Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"),
                                           (120, 155),
                                           id="Fri Sep  4 21_40_27 2026 => position: (298515, 221476, 10289, 270, 269)"),
                              # TODO: rename
                              ], indirect=['minimap_image'])
    def test_finds_path_to_visible_water_shore(self, minimap_image, expected_location, extras):
        minimap = MinimapAnalyzer().analyze(MinimapCapture.capture)
        result = LocalNavigator().find_nearest_water(MinimapCapture.capture)
        extras.append(
            pytest_html.extras.image(base_image_array(MinimapCapture.draw_mask(minimap, result.player), mode='RGB')))
        extras.append(
            pytest_html.extras.image(base_image_array(MinimapCapture.draw_mask(minimap, result.target), mode='RGB')))
        extras.append(pytest_html.extras.image(
            base_image_array(MinimapCapture.draw_mask(minimap, result.water_mask), mode='RGB')))
        extras.append(
            pytest_html.extras.image(base_image_array(MinimapCapture.draw_mask(minimap, result.road_mask), mode='RGB')))
        assert result.target is not None
        assert result.path
