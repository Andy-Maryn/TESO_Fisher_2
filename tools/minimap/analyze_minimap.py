"""Analyze a minimap image and save a debug visualization.

Usage:
    python tools/minimap/analyze_minimap.py path/to/fullscreen.jpeg output.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from navigation.minimap import LocalNavigator, MinimapAnalyzer, MinimapRegion, draw_debug


def extract_minimap(image):
    region = MinimapRegion()
    return image[region.top:region.bottom, region.left:region.right]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    fullscreen = cv2.cvtColor(cv2.imread(str(args.image)), cv2.COLOR_BGR2RGB)
    minimap = extract_minimap(fullscreen)

    analyzer = MinimapAnalyzer()
    local_map = analyzer.analyze(minimap)
    result = LocalNavigator(analyzer=analyzer).find_nearest_water(minimap)

    output = draw_debug(local_map, result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.output), cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

    print(f"player={result.player}")
    print(f"water_pixels={int(result.water_mask.sum())}")
    print(f"road_pixels={int(result.road_mask.sum())}")
    print(f"target={result.target}")
    print(f"path_points={len(result.path)}")
    print(f"next_bearing={result.bearing_to_next_waypoint()}")
    print(f"debug={args.output}")


if __name__ == "__main__":
    main()
