"""Small standalone regression tests for the minimap CV pipeline."""
from pathlib import Path

import cv2

from navigation.minimap import LocalNavigator, MinimapAnalyzer


SAMPLE = next((Path(__file__).parent / "data_screen_capture" / "coords_and_heading").glob("*.jpeg"))


def load_minimap():
    image = cv2.imread(str(SAMPLE))
    if image is None:
        raise AssertionError(f"Could not load sample: {SAMPLE}")
    return cv2.cvtColor(image[0:280, 1640:1920], cv2.COLOR_BGR2RGB)


def test_detects_large_water_area():
    minimap = MinimapAnalyzer().analyze(load_minimap())
    assert minimap.water_mask.sum() > 5_000


def test_detects_player_near_minimap_center():
    player = MinimapAnalyzer().analyze(load_minimap()).player
    assert 120 <= player[0] <= 155
    assert 120 <= player[1] <= 155


def test_finds_path_to_visible_water_shore():
    result = LocalNavigator().find_nearest_water(load_minimap())
    assert result.target is not None
    assert result.path
