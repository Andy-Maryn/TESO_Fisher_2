import math
from typing import Callable

import numpy as np
from PIL import Image, ImageFilter

from luaParser.yet_another_compass_parser import YetAnotherCompassParser as yacp
from moving.moving import Moving
from screenCapture.screen_capture import ScreeCapture


class YetAnotherCompassCapture(ScreeCapture):
    main_color = np.array([10, 163, 48])

    @classmethod
    def get_cap(cls, **kwargs):
        super().get_cap(
            point_left=yacp.left_point,
            point_top=yacp.top_point,
            point_right=yacp.right_point,
            point_bottom=yacp.bottom_point)

    @classmethod
    def get_tip(cls) -> tuple[int, int]:
        cls.capture = Image.fromarray(cls.capture).filter(ImageFilter.MaxFilter(3))
        cls.capture = np.asarray(cls.capture)

        _to = yacp.size // 3
        _from = yacp.size - (yacp.size // 3)

        direction_minor = range(0, yacp.size)

        direction_major: range
        forward_direction = range(0, yacp.size, 1)
        inverse_direction = range(yacp.size - 1, 0, -1)  # for bottom

        direction_axes: Callable
        direction_axes_x: Callable = lambda x, i, j: (x[i, j, 0], i, j)
        direction_axes_y: Callable = lambda x, i, j: (x[j, i, 0], j, i)

        left = ((yacp.size // 3) * yacp.size) - np.sum(cls.capture[:, :_to, 0] // 255)
        right = ((yacp.size // 3) * yacp.size) - np.sum(cls.capture[:, _from:, 0] // 255)
        top = ((yacp.size // 3) * yacp.size) - np.sum(cls.capture[:_to, :, 0] // 255)
        bottom = ((yacp.size // 3) * yacp.size) - np.sum(cls.capture[_from:, :, 0] // 255)

        current_side = max(left, right, top, bottom)

        if current_side == left:
            direction_major = forward_direction
            direction_axes = direction_axes_y
        elif current_side == right:
            direction_major = inverse_direction
            direction_axes = direction_axes_y

        elif current_side == top:
            direction_major = forward_direction
            direction_axes = direction_axes_x
        elif current_side == bottom:
            direction_major = inverse_direction
            direction_axes = direction_axes_x
        else:
            raise

        def find_point(direction: range, axes: Callable) -> tuple[int, int] | None:
            for i in direction:
                for j in direction_minor:
                    coord, x, y = axes(cls.capture, i, j)
                    if coord < 100:  # TODO: should be 0, but 4 is min value
                        return x, y
            return None

        return find_point(direction_major, direction_axes)

    @classmethod
    def get_segment_length(cls) -> float | None:
        """
          0,   0 -> -75,  75
        150, 150 ->  75, -75
        :return:
        """
        mid_point = yacp.size // 2
        x_axes = lambda x: x - mid_point
        y_axes = lambda x: mid_point - x

        tip = cls.get_tip()

        if tip is not None:
            y, x = tip
            x = x_axes(x)
            y = y_axes(y)

            degree = Moving.get_degree((0, 0), (x, y))
            return degree

        return None
