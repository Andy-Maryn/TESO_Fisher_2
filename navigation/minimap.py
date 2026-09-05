"""Classical-computer-vision navigation for the ESO minimap.

The module intentionally does not use ML.  It extracts a local semantic map
from the minimap image, detects water/road regions, and can plan a path to the
nearest shore using A*.
"""
from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageGrab


@dataclass(frozen=True)
class MinimapRegion:
    left: int = 1640
    top: int = 0
    right: int = 1920
    bottom: int = 280

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top


@dataclass(frozen=True)
class MinimapConfig:
    region: MinimapRegion = MinimapRegion()
    map_border: int = 7
    player_hue_min: int = 80
    player_hue_max: int = 110
    water_hue_min: int = 85
    water_hue_max: int = 179
    water_saturation_min: int = 35
    water_value_min: int = 65
    road_red_min: int = 195
    road_green_min: int = 165
    road_blue_min: int = 105
    road_red_green_max_diff: int = 55
    road_green_blue_min_diff: int = 20
    min_water_component_area: int = 150
    min_road_component_area: int = 12
    road_dilation: int = 2
    water_dilation: int = 2
    path_scale: int = 2


@dataclass
class MinimapMap:
    image: np.ndarray
    player: tuple[int, int]
    road_mask: np.ndarray
    water_mask: np.ndarray

    @property
    def walkable_mask(self) -> np.ndarray:
        # The actual border width is supplied by the analyzer configuration
        # when the map is created; the default is 7 px for the current ESO UI.
        walkable = ~self.water_mask.copy()
        border = 7
        walkable[:border, :] = False
        walkable[-border:, :] = False
        walkable[:, :border] = False
        walkable[:, -border:] = False
        return walkable


@dataclass
class NavigationResult:
    path: list[tuple[int, int]]
    target: tuple[int, int] | None
    player: tuple[int, int]
    road_mask: np.ndarray
    water_mask: np.ndarray

    @property
    def reached_water_shore(self) -> bool:
        return self.target is not None and bool(self.path)

    def bearing_to_next_waypoint(self, look_ahead: int = 8) -> float | None:
        """Return minimap bearing where 0=up, +90=right, -90=left."""
        if not self.path:
            return None
        index = min(max(1, look_ahead), len(self.path) - 1)
        x0, y0 = self.player
        x1, y1 = self.path[index]
        dx = x1 - x0
        dy = y1 - y0
        return math.degrees(math.atan2(dx, -dy))


class MinimapCapture:
    """Capture the configured minimap directly from the desktop."""

    def __init__(self, config: MinimapConfig | None = None) -> None:
        self.config = config or MinimapConfig()

    def capture(self) -> np.ndarray:
        region = self.config.region
        image = ImageGrab.grab(
            bbox=(region.left, region.top, region.right, region.bottom)
        ).convert("RGB")
        return np.asarray(image)


class MinimapAnalyzer:
    """Detect map semantics using deterministic OpenCV processing."""

    def __init__(self, config: MinimapConfig | None = None) -> None:
        self.config = config or MinimapConfig()

    @staticmethod
    def _filter_components(mask: np.ndarray, min_area: int) -> np.ndarray:
        count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        result = np.zeros_like(mask)
        for label in range(1, count):
            area = int(stats[label, cv2.CC_STAT_AREA])
            if area >= min_area:
                result[labels == label] = 255
        return result

    def _detect_water(self, image_bgr: np.ndarray) -> np.ndarray:
        # In the supplied ESO minimap water is green/cyan rather than the
        # yellow/brown palette used by land.  The RGB relationship is more
        # stable than relying on a single exact hue.
        blurred = cv2.GaussianBlur(image_bgr, (9, 9), 0)
        blue, green, red = cv2.split(blurred)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        green_minus_red = green.astype(np.int16) - red.astype(np.int16)
        blue_minus_red = blue.astype(np.int16) - red.astype(np.int16)

        mask = (
            (hsv[..., 0] >= 28)
            & (hsv[..., 0] <= 50)
            & (hsv[..., 1] >= 20)
            & (hsv[..., 1] <= 150)
            & (hsv[..., 2] >= 120)
            & (green_minus_red >= 0)
            & (blue_minus_red >= -80)
        )
        mask = mask.astype(np.uint8) * 255

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = self._filter_components(mask, self.config.min_water_component_area)

        border = self.config.map_border
        mask[:border, :] = 0
        mask[-border:, :] = 0
        mask[:, :border] = 0
        mask[:, -border:] = 0
        return mask.astype(bool)

    def _detect_road(self, image_bgr: np.ndarray, water_mask: np.ndarray) -> np.ndarray:
        """Detect ESO road strokes using their characteristic light/warm color.

        The previous local-contrast detector also selected terrain borders,
        texture and decorative map lines. Roads on the bundled ESO minimap
        are much more consistently identified by color: they are light,
        warm/pale strokes on darker brown terrain.
        """
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        r = image_rgb[..., 0].astype(np.int16)
        g = image_rgb[..., 1].astype(np.int16)
        b = image_rgb[..., 2].astype(np.int16)

        # Pale warm road pixels. Keep this deliberately narrow so terrain
        # texture and dark contour lines are not classified as roads.
        mask = (
            (r >= self.config.road_red_min)
            & (g >= self.config.road_green_min)
            & (b >= self.config.road_blue_min)
            & ((r - g) <= self.config.road_red_green_max_diff)
            & ((g - b) >= self.config.road_green_blue_min_diff)
        )

        mask &= ~water_mask
        mask = (mask.astype(np.uint8) * 255)

        # Join neighboring pixels belonging to the same road stroke.
        close_kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (5, 5)
        )
        open_kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (3, 3)
        )
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel, iterations=1)

        # Small compact components are usually map icons rather than roads.
        count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        filtered = np.zeros_like(mask)
        for label in range(1, count):
            area = int(stats[label, cv2.CC_STAT_AREA])
            width = int(stats[label, cv2.CC_STAT_WIDTH])
            height = int(stats[label, cv2.CC_STAT_HEIGHT])
            longest = max(width, height)
            shortest = max(1, min(width, height))
            elongated = longest / shortest >= 1.5
            if area >= self.config.min_road_component_area and (elongated or area >= 80):
                filtered[labels == label] = 255

        if self.config.road_dilation > 0:
            size = self.config.road_dilation * 2 + 1
            dilation_kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (size, size)
            )
            filtered = cv2.dilate(filtered, dilation_kernel)

        border = self.config.map_border
        filtered[:border, :] = 0
        filtered[-border:, :] = 0
        filtered[:, :border] = 0
        filtered[:, -border:] = 0
        return filtered.astype(bool)

    def _detect_player(self, image_bgr: np.ndarray) -> tuple[int, int]:
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            hsv,
            np.array([self.config.player_hue_min, 100, 90], dtype=np.uint8),
            np.array([self.config.player_hue_max, 255, 255], dtype=np.uint8),
        )
        count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, 8)

        best_label = None
        best_area = 0
        for label in range(1, count):
            area = int(stats[label, cv2.CC_STAT_AREA])
            width = int(stats[label, cv2.CC_STAT_WIDTH])
            height = int(stats[label, cv2.CC_STAT_HEIGHT])
            if 10 <= area <= 200 and width <= 30 and height <= 30 and area > best_area:
                best_area = area
                best_label = label

        if best_label is not None:
            x, y = centroids[best_label]
            return int(round(x)), int(round(y))

        # The ESO player marker is normally centered on the minimap.
        h, w = image_bgr.shape[:2]
        return w // 2, h // 2

    def analyze(self, image: np.ndarray | str | Path) -> MinimapMap:
        if isinstance(image, (str, Path)):
            image_rgb = np.asarray(Image.open(image).convert("RGB"))
        else:
            image_rgb = np.asarray(image)
            if image_rgb.ndim != 3 or image_rgb.shape[2] != 3:
                raise ValueError("Expected an RGB image with shape HxWx3")

        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        water = self._detect_water(image_bgr)
        road = self._detect_road(image_bgr, water)
        player = self._detect_player(image_bgr)
        return MinimapMap(image_rgb, player, road, water)


class AStarPlanner:
    """A* planner over a local minimap cost grid."""

    _NEIGHBOURS: tuple[tuple[int, int, float], ...] = (
        (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
        (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),
        (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2)),
    )

    def __init__(self, scale: int = 2) -> None:
        if scale < 1:
            raise ValueError("scale must be >= 1")
        self.scale = scale

    def _downsample_mask(self, mask: np.ndarray) -> np.ndarray:
        h, w = mask.shape
        return cv2.resize(
            mask.astype(np.uint8),
            (max(1, w // self.scale), max(1, h // self.scale)),
            interpolation=cv2.INTER_AREA,
        ) > 0.5

    @staticmethod
    def _heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def plan(
        self,
        walkable_mask: np.ndarray,
        road_mask: np.ndarray,
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        walkable = self._downsample_mask(walkable_mask)
        road = self._downsample_mask(road_mask)
        h, w = walkable.shape

        start_grid = (
            max(0, min(w - 1, start[0] // self.scale)),
            max(0, min(h - 1, start[1] // self.scale)),
        )
        goal_grid = (
            max(0, min(w - 1, goal[0] // self.scale)),
            max(0, min(h - 1, goal[1] // self.scale)),
        )

        if not walkable[start_grid[1], start_grid[0]]:
            start_grid = self._nearest_walkable(walkable, start_grid)
        if not walkable[goal_grid[1], goal_grid[0]]:
            goal_grid = self._nearest_walkable(walkable, goal_grid)

        frontier: list[tuple[float, int, tuple[int, int]]] = []
        sequence = 0
        heappush(frontier, (0.0, sequence, start_grid))
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {start_grid: None}
        cost_so_far: dict[tuple[int, int], float] = {start_grid: 0.0}

        while frontier:
            _, _, current = heappop(frontier)
            if current == goal_grid:
                break

            cx, cy = current
            for dx, dy, step_cost in self._NEIGHBOURS:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                if not walkable[ny, nx]:
                    continue

                # Roads are preferred, but leaving the road remains allowed.
                terrain_cost = 0.75 if road[ny, nx] else 1.5
                new_cost = cost_so_far[current] + step_cost * terrain_cost
                neighbour = (nx, ny)
                if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                    cost_so_far[neighbour] = new_cost
                    sequence += 1
                    priority = new_cost + self._heuristic(neighbour, goal_grid)
                    heappush(frontier, (priority, sequence, neighbour))
                    came_from[neighbour] = current

        if goal_grid not in came_from:
            return []

        grid_path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = goal_grid
        while current is not None:
            grid_path.append(current)
            current = came_from[current]
        grid_path.reverse()

        return [
            (
                min(walkable_mask.shape[1] - 1, x * self.scale + self.scale // 2),
                min(walkable_mask.shape[0] - 1, y * self.scale + self.scale // 2),
            )
            for x, y in grid_path
        ]

    @staticmethod
    def _nearest_walkable(
        walkable: np.ndarray,
        point: tuple[int, int],
    ) -> tuple[int, int]:
        ys, xs = np.where(walkable)
        if len(xs) == 0:
            raise ValueError("The minimap contains no walkable cells")
        distances = (xs - point[0]) ** 2 + (ys - point[1]) ** 2
        index = int(np.argmin(distances))
        return int(xs[index]), int(ys[index])


class LocalNavigator:
    """Build a route from the player to the nearest visible water shore."""

    def __init__(
        self,
        analyzer: MinimapAnalyzer | None = None,
        planner: AStarPlanner | None = None,
    ) -> None:
        self.analyzer = analyzer or MinimapAnalyzer()
        self.planner = planner or AStarPlanner(self.analyzer.config.path_scale)

    def _nearest_shore(
        self,
        minimap: MinimapMap,
    ) -> tuple[int, int] | None:
        water = minimap.water_mask
        if not water.any():
            return None

        water_uint8 = water.astype(np.uint8) * 255
        kernel_size = self.analyzer.config.water_dilation * 2 + 1
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
        )
        near_water = cv2.dilate(water_uint8, kernel) > 0
        shore = near_water & minimap.walkable_mask

        ys, xs = np.where(shore)
        if len(xs) == 0:
            return None

        px, py = minimap.player
        distances = (xs - px) ** 2 + (ys - py) ** 2
        index = int(np.argmin(distances))
        return int(xs[index]), int(ys[index])

    def plan_to_point(
        self,
        image: np.ndarray | str | Path,
        target: tuple[int, int],
    ) -> NavigationResult:
        minimap = self.analyzer.analyze(image)
        path = self.planner.plan(
            minimap.walkable_mask,
            minimap.road_mask,
            minimap.player,
            target,
        )
        return NavigationResult(
            path=path,
            target=target,
            player=minimap.player,
            road_mask=minimap.road_mask,
            water_mask=minimap.water_mask,
        )

    def find_nearest_water(self, image: np.ndarray | str | Path) -> NavigationResult:
        minimap = self.analyzer.analyze(image)
        target = self._nearest_shore(minimap)
        if target is None:
            return NavigationResult(
                path=[],
                target=None,
                player=minimap.player,
                road_mask=minimap.road_mask,
                water_mask=minimap.water_mask,
            )
        return self.plan_to_point(minimap.image, target)


def draw_debug(
    minimap: MinimapMap,
    result: NavigationResult | None = None,
) -> np.ndarray:
    """Return an RGB debug image with detected water, roads and optional path."""
    overlay = minimap.image.copy()

    # Water: blue tint; road: magenta tint.
    water_color = np.array([60, 150, 255], dtype=np.uint8)
    road_color = np.array([255, 80, 190], dtype=np.uint8)
    overlay[minimap.water_mask] = (
        0.55 * overlay[minimap.water_mask] + 0.45 * water_color
    ).astype(np.uint8)
    overlay[minimap.road_mask] = (
        0.55 * overlay[minimap.road_mask] + 0.45 * road_color
    ).astype(np.uint8)

    px, py = minimap.player
    cv2.circle(overlay, (px, py), 5, (255, 255, 0), 2)

    if result is not None and result.path:
        points = np.asarray(result.path, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(overlay, [points], False, (0, 255, 0), 2)
        if result.target is not None:
            cv2.circle(overlay, result.target, 5, (255, 0, 0), -1)

    return overlay
