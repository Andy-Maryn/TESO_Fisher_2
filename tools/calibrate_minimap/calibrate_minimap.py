"""Interactive HSV calibration tool for the ESO minimap.

Usage:
    python calibrate_minimap.py "path/to/full_screen.jpeg"

Keys:
    r - road calibration
    w - water calibration
    s - save current calibration to minimap_calibration.json
    q / ESC - quit

The tool deliberately does not modify the navigation code. It is only used to
find stable HSV thresholds on real screenshots.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

WINDOW = "TESO minimap calibration"
CONFIG_NAME = "minimap_calibration.json"


def nothing(_: int) -> None:
    pass


def create_trackbars() -> None:
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW, 900, 700)

    for name, value, maximum in (
            ("H min", 0, 179), ("H max", 30, 179),
            ("S min", 0, 255), ("S max", 160, 255),
            ("V min", 120, 255), ("V max", 255, 255),
            ("Min area", 20, 5000),
    ):
        cv2.createTrackbar(name, WINDOW, value, maximum, nothing)


def get_thresholds() -> dict[str, int]:
    return {
        name: cv2.getTrackbarPos(name, WINDOW)
        for name in ("H min", "H max", "S min", "S max", "V min", "V max", "Min area")
    }


def set_thresholds(values: dict[str, int]) -> None:
    for name, value in values.items():
        cv2.setTrackbarPos(name, WINDOW, int(value))


def make_mask(hsv: np.ndarray, values: dict[str, int]) -> np.ndarray:
    h_min, h_max = values["H min"], values["H max"]
    s_min, s_max = values["S min"], values["S max"]
    v_min, v_max = values["V min"], values["V max"]

    if h_min <= h_max:
        mask = (
                (hsv[..., 0] >= h_min)
                & (hsv[..., 0] <= h_max)
                & (hsv[..., 1] >= s_min)
                & (hsv[..., 1] <= s_max)
                & (hsv[..., 2] >= v_min)
                & (hsv[..., 2] <= v_max)
        )
    else:
        # Hue interval crossing 0, e.g. 170..10.
        mask = (
                ((hsv[..., 0] >= h_min) | (hsv[..., 0] <= h_max))
                & (hsv[..., 1] >= s_min)
                & (hsv[..., 1] <= s_max)
                & (hsv[..., 2] >= v_min)
                & (hsv[..., 2] <= v_max)
        )

    mask = mask.astype(np.uint8) * 255

    min_area = max(1, values["Min area"])
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    filtered = np.zeros_like(mask)
    for label in range(1, count):
        if int(stats[label, cv2.CC_STAT_AREA]) >= min_area:
            filtered[labels == label] = 255

    return filtered


def overlay(image_bgr: np.ndarray, mask: np.ndarray) -> np.ndarray:
    result = image_bgr.copy()
    result[mask > 0] = (255, 0, 255)
    return result


def crop_minimap(image_bgr: np.ndarray) -> np.ndarray:
    # Current ESO 1920x1080 layout.
    if image_bgr.shape[1] < 1920 or image_bgr.shape[0] < 280:
        raise ValueError(
            f"Expected a 1920x1080 (or larger) screenshot, got "
            f"{image_bgr.shape[1]}x{image_bgr.shape[0]}"
        )
    return image_bgr[0:280, 1640:1920]


def save_config(path: Path, road: dict[str, int], water: dict[str, int]) -> None:
    data = {
        "road": road,
        "water": water,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Saved calibration: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(CONFIG_NAME),
        help="JSON file to write with calibrated thresholds",
    )
    args = parser.parse_args()

    image = cv2.imread(str(args.image))
    if image is None:
        raise FileNotFoundError(args.image)

    minimap = crop_minimap(image)
    hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)

    create_trackbars()

    road = {
        "H min": 10, "H max": 28,
        "S min": 35, "S max": 150,
        "V min": 205, "V max": 255,
        "Min area": 20,
    }
    water = {
        "H min": 28, "H max": 50,
        "S min": 20, "S max": 150,
        "V min": 120, "V max": 255,
        "Min area": 150,
    }

    mode = "road"
    set_thresholds(road)

    while True:
        values = get_thresholds()

        if mode == "road":
            road = values
        else:
            water = values

        mask = make_mask(hsv, values)
        view = overlay(minimap, mask)

        title = (
            f"{mode.upper()} | "
            "R=road W=water S=save Q=quit | "
            f"pixels={int((mask > 0).sum())}"
        )
        cv2.putText(
            view,
            title,
            (8, 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (0, 0, 0),
            3,
            cv2.LINE_AA,
        )
        cv2.putText(
            view,
            title,
            (8, 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        cv2.imshow(WINDOW, view)
        key = cv2.waitKey(30) & 0xFF

        if key in (27, ord("q")):
            break

        if key == ord("r") and mode != "road":
            water = values
            mode = "road"
            set_thresholds(road)

        elif key == ord("w") and mode != "water":
            road = values
            mode = "water"
            set_thresholds(water)

        elif key == ord("s"):
            save_config(args.output, road, water)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
