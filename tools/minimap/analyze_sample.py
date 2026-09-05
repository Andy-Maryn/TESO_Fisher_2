"""Analyze the first bundled fullscreen screenshot."""
from pathlib import Path

import cv2

from navigation.minimap import LocalNavigator, MinimapAnalyzer, MinimapRegion, draw_debug


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "tests" / "data_screen_capture" / "coords_and_heading"
OUTPUT = ROOT.parent / "minimap_navigation_debug.png"


def main() -> None:
    source = next(DATA.glob("*.jpeg"))
    image_bgr = cv2.imread(str(source))
    if image_bgr is None:
        raise RuntimeError(f"Cannot read {source}")

    region = MinimapRegion()
    minimap = image_bgr[region.top:region.bottom, region.left:region.right]
    minimap_rgb = cv2.cvtColor(minimap, cv2.COLOR_BGR2RGB)

    analyzer = MinimapAnalyzer()
    detected = analyzer.analyze(minimap_rgb)
    result = LocalNavigator(analyzer=analyzer).find_nearest_water(minimap_rgb)
    debug = draw_debug(detected, result)

    cv2.imwrite(str(OUTPUT), cv2.cvtColor(debug, cv2.COLOR_RGB2BGR))
    print(f"source={source}")
    print(f"player={result.player}")
    print(f"water_pixels={int(result.water_mask.sum())}")
    print(f"road_pixels={int(result.road_mask.sum())}")
    print(f"water_shore_target={result.target}")
    print(f"path_points={len(result.path)}")
    print(f"next_bearing={result.bearing_to_next_waypoint()}")
    print(f"debug={OUTPUT}")


if __name__ == "__main__":
    main()
