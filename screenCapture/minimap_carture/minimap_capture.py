"""Minimap capture"""
import cv2

from navigation.minimap import MinimapAnalyzer, MinimapMap
from screenCapture.screen_capture import *


class MinimapCapture(ScreeCapture):
    """Capture the configured minimap directly from the desktop."""

    @classmethod
    def get_cap(cls, **kwargs) -> ndarray[Any, dtype[Any]]:
        """Capture the coordinates/heading area."""
        super().get_cap(point_left=1640,
                        point_top=0,
                        point_right=1920,
                        point_bottom=280)
        return cls.capture

    @classmethod
    def draw_player(cls, minimap) -> ndarray[Any, dtype[Any]]:
        """Draw the player."""
        image = minimap.image.copy()
        cv2.circle(
            image,
            minimap.player,
            5,
            (255, 0, 0),
            -1,
        )
        return image

    @classmethod
    def draw_target(cls, minimap, result) -> ndarray[Any, dtype[Any]]:
        """Draw the target."""
        image = minimap.image.copy()
        cv2.circle(
            image,
            result.target,
            5,
            (255, 0, 0),
            -1,
        )
        return image

    @classmethod
    def draw_water(cls, minimap):
        """Draw the water."""
        debug_image = minimap.image.copy()

        debug_image = cls._overlay_mask(
            debug_image,
            minimap.water_mask,
            color=(0, 255, 0),
            alpha=0.35,
        )
        return debug_image

    @classmethod
    def draw_road(cls, minimap):
        """Draw the road."""
        debug_image = minimap.image.copy()

        debug_image = cls._overlay_mask(
            debug_image,
            minimap.road_mask,
            color=(255, 255, 0),
            alpha=0.5,
        )
        return debug_image

    @classmethod
    def _overlay_mask(cls,
            minimap: MinimapMap,
            mask: np.ndarray,
            color: tuple[int, int, int],
            alpha: float = 0.4,
    ) -> np.ndarray:
        """Overlay a colored boolean mask on an RGB image."""
        color_layer = np.zeros_like(minimap)
        color_layer[mask] = color

        cv2.addWeighted(
            color_layer,
            alpha,
            minimap,
            1.0 - alpha,
            0,
            dst=minimap,
        )

        return minimap
