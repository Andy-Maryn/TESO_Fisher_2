from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class RoadDetectorConfig:
    hue_min: int = 15
    hue_max: int = 24
    saturation_min: int = 60
    saturation_max: int = 130
    value_min: int = 210
    value_max: int = 255
    min_component_area: int = 35
    min_major_axis: int = 10
    min_aspect_ratio: float = 2.0
    open_kernel: int = 3
    close_kernel: int = 3
    ray_length: int = 70
    ray_width: int = 5
    angle_step: int = 5


@dataclass
class RoadDetection:
    candidates: np.ndarray
    road_mask: np.ndarray
    direction_scores: list[tuple[float, float]]
    best_angle: float | None


class RoadDetector:
    def __init__(self, config: RoadDetectorConfig | None = None):
        self.config = config or RoadDetectorConfig()

    def detect(self, image: np.ndarray, player: tuple[int, int]) -> RoadDetection:
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        c = self.config
        candidates = cv2.inRange(hsv,
                                 (c.hue_min, c.saturation_min, c.value_min),
                                 (c.hue_max, c.saturation_max, c.value_max))
        mask = self._geometry_filter(candidates)
        if c.open_kernel > 1:
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (c.open_kernel, c.open_kernel))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
        if c.close_kernel > 1:
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (c.close_kernel, c.close_kernel))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
        scores = self._direction_scores(mask, player)
        best = max(scores, key=lambda x: x[1])[0] if scores else None
        return RoadDetection(candidates, mask, scores, best)

    def _geometry_filter(self, mask: np.ndarray) -> np.ndarray:
        c = self.config
        n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        out = np.zeros_like(mask)
        for label in range(1, n):
            area = int(stats[label, cv2.CC_STAT_AREA])
            w = int(stats[label, cv2.CC_STAT_WIDTH])
            h = int(stats[label, cv2.CC_STAT_HEIGHT])
            major, minor = max(w, h), max(1, min(w, h))
            if (
                    area >= c.min_component_area
                    and major >= c.min_major_axis
                    and major / minor >= c.min_aspect_ratio
            ):
                out[labels == label] = 255
        return out

    def _direction_scores(self, mask: np.ndarray, player: tuple[int, int]):
        px, py = player
        h, w = mask.shape
        c = self.config
        result = []
        for angle in range(-90, 91, c.angle_step):
            a = np.deg2rad(angle)
            dx, dy = np.sin(a), -np.cos(a)
            hit = total = 0
            for d in range(8, c.ray_length + 1, 2):
                x, y = round(px + dx * d), round(py + dy * d)
                if not (0 <= x < w and 0 <= y < h): break
                patch = mask[max(0, y - c.ray_width):min(h, y + c.ray_width + 1),
                        max(0, x - c.ray_width):min(w, x + c.ray_width + 1)]
                total += patch.size
                hit += int(np.count_nonzero(patch))
            result.append((float(angle), hit / total if total else 0.0))
        return result


def load_image(path: str | Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None: raise FileNotFoundError(path)
    return image


def draw_debug(image, detection: RoadDetection, player):
    out = image.copy()
    raw = np.zeros_like(out);
    raw[detection.candidates > 0] = (0, 0, 255)
    road = np.zeros_like(out);
    road[detection.road_mask > 0] = (0, 255, 0)
    out = cv2.addWeighted(out, 1.0, raw, .25, 0)
    out = cv2.addWeighted(out, 1.0, road, .65, 0)
    px, py = player
    cv2.circle(out, (px, py), 5, (255, 255, 255), -1)
    if detection.best_angle is not None:
        a = np.deg2rad(detection.best_angle)
        end = (round(px + np.sin(a) * 55), round(py - np.cos(a) * 55))
        cv2.arrowedLine(out, (px, py), end, (255, 255, 255), 2, tipLength=.2)
    return out
