from typing import Callable

import numpy as np
from PIL import Image, ImageFilter

from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from screenCapture.screen_capture import ScreeCapture


class YetAnotherCompassCapture(ScreeCapture):
    main_color = np.array([10, 163, 48])

    @classmethod
    def get_cap(cls, **kwargs):
        super().get_cap(
            point_left=YetAnotherCompassParser.left_point,
            point_top=YetAnotherCompassParser.top_point,
            point_right=YetAnotherCompassParser.right_point,
            point_bottom=YetAnotherCompassParser.bottom_point)

    @classmethod
    def get_tip(cls) -> tuple[int, int]:
        cls.capture = Image.fromarray(cls.capture).filter(ImageFilter.MaxFilter(3))
        cls.capture = np.asarray(cls.capture)
        
        _size = YetAnotherCompassParser.size
        _to = _size // 3
        _from = _size - _to

        direction_minor = range(0, _size)

        direction_major: range
        forward_direction = range(0, _size, 1)
        inverse_direction = range(_size - 1, 0, -1)  # for bottom

        direction_axes: Callable
        direction_axes_x: Callable = lambda x, i, j: (x[i, j, 0], i, j)
        direction_axes_y: Callable = lambda x, i, j: (x[j, i, 0], j, i)

        left = (_to * _size) - np.sum(cls.capture[:, :_to, 0] // 255)
        right = (_to * _size) - np.sum(cls.capture[:, _from:, 0] // 255)
        top = (_to * _size) - np.sum(cls.capture[:_to, :, 0] // 255)
        bottom = (_to * _size) - np.sum(cls.capture[_from:, :, 0] // 255)

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
    def get_compas_direction(cls) -> tuple[float, float] | None:
        """
          0,   0 -> -75,  75
        150, 150 ->  75, -75
        :return:
        """
        mid_point = YetAnotherCompassParser.size // 2
        x_axes: Callable[[int], int] = lambda _x: _x - mid_point
        y_axes: Callable[[int], int] = lambda _y: mid_point - _y

        tip = cls.get_tip()

        if tip is not None:
            y, x = tip
            x = x_axes(x)
            y = y_axes(y)
            return x, y

        return None
