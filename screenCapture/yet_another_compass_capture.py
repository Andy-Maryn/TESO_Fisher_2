from enum import Enum
from importlib.resources import read_text
from typing import Callable

import numpy as np
from PIL import Image, ImageFilter

from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from screenCapture.screen_capture import ScreeCapture

class CardinalDirections(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'

class YetAnotherCompassCapture(ScreeCapture):
    #main_color = np.array([10, 163, 48])
    main_color = np.array([0, 0, 0])

    @classmethod
    def get_cap(cls, **kwargs):
        super().get_cap(
            point_left=YetAnotherCompassParser.left_point,
            point_top=YetAnotherCompassParser.top_point,
            point_right=YetAnotherCompassParser.right_point,
            point_bottom=YetAnotherCompassParser.bottom_point)

    @classmethod
    def get_cardinal_directions(cls) -> CardinalDirections:
        _size = YetAnotherCompassParser.size
        _to = _size // 3
        _from = _size - _to

        cardinal_directions: dict[int, CardinalDirections] ={
            np.sum(cls.capture[:, :_to]): CardinalDirections.LEFT,
            np.sum(cls.capture[:, _from:]): CardinalDirections.RIGHT,
            np.sum(cls.capture[:_to, :]): CardinalDirections.TOP,
            np.sum(cls.capture[_from:, :]):CardinalDirections.BOTTOM
        }

        current_side = max(cardinal_directions.keys())
        return cardinal_directions.get(current_side)

    @classmethod
    def get_tip(cls, current_side: CardinalDirections) -> tuple[int, int]:
        _size = YetAnotherCompassParser.size

        direction_minor = range(0, _size)

        direction_major: range
        forward_direction = range(0, _size, 1)
        inverse_direction = range(_size - 1, 0, -1)  # for bottom

        direction_axes: Callable
        direction_axes_x: Callable = lambda x, i, j: (x[i, j], i, j)
        direction_axes_y: Callable = lambda x, i, j: (x[j, i], j, i)

        if current_side == CardinalDirections.LEFT:
            direction_major = forward_direction
            direction_axes = direction_axes_y
        elif current_side == CardinalDirections.RIGHT:
            direction_major = inverse_direction
            direction_axes = direction_axes_y
        elif current_side == CardinalDirections.TOP:
            direction_major = forward_direction
            direction_axes = direction_axes_x
        elif current_side == CardinalDirections.BOTTOM:
            direction_major = inverse_direction
            direction_axes = direction_axes_x
        else:
            raise

        def find_point(direction: range, axes: Callable) -> tuple[int, int] | None:
            for i in direction:
                for j in direction_minor:
                    coord, x, y = axes(cls.capture, i, j)
                    # if coord < 100:  # TODO: should be 0, but 4 is min value
                    #     return x, y
                    if coord == 1:
                        return x, y
            return None

        return find_point(direction_major, direction_axes)

    @classmethod
    def get_compas_direction(cls, tip: tuple[int, int]) -> tuple[float, float] | None:
        """
          0,   0 -> -75,  75
        150, 150 ->  75, -75
        :return:
        """
        #cls.get_cap()
        mid_point = YetAnotherCompassParser.size // 2
        x_axes: Callable[[int], int] = lambda _x: _x - mid_point
        y_axes: Callable[[int], int] = lambda _y: mid_point - _y

        if tip is not None:
            y, x = tip
            x = x_axes(x)
            y = y_axes(y)
            return x, y

        return None
