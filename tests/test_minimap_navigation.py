from pathlib import Path

import cv2
import numpy as np

from navigation.minimap import LocalNavigator, MinimapAnalyzer, draw_debug


DATA_DIR = Path(__file__).parent / "data_screen_capture" / "coords_and_heading"
SAMPLE = DATA_DIR / "Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"


def _crop_minimap(image: np.ndarray) -> np.ndarray:
    # Coordinates of the ESO minimap in the supplied 1920x1080 test screenshot.
    return image[0:280, 1640:1920]


def test_minimap_detects_player_and_water():
    image = cv2.cvtColor(cv2.imread(str(SAMPLE)), cv2.COLOR_BGR2RGB)
    minimap = MinimapAnalyzer().analyze(_crop_minimap(image))

    px, py = minimap.player
    assert 120 <= px <= 155
    assert 120 <= py <= 155
    assert minimap.water_mask.sum() > 5_000
    assert minimap.road_mask.sum() > 500


def test_minimap_finds_water_shore_and_path():
    image = cv2.cvtColor(cv2.imread(str(SAMPLE)), cv2.COLOR_BGR2RGB)
    minimap = MinimapAnalyzer().analyze(_crop_minimap(image))
    result = LocalNavigator().find_nearest_water(_crop_minimap(image))

    assert result.target is not None
    assert result.path
    assert result.path[0][0] >= 0
    assert result.path[0][1] >= 0
    assert result.water_mask.sum() > 5_000


def test_minimap_debug_image_can_be_saved(tmp_path):
    image = cv2.cvtColor(cv2.imread(str(SAMPLE)), cv2.COLOR_BGR2RGB)
    minimap = MinimapAnalyzer().analyze(_crop_minimap(image))
    result = LocalNavigator().find_nearest_water(_crop_minimap(image))
    debug = draw_debug(minimap, result)

    output = tmp_path / "minimap_navigation_debug.png"
    cv2.imwrite(str(output), cv2.cvtColor(debug, cv2.COLOR_RGB2BGR))

    assert output.exists()
    assert output.stat().st_size > 0
