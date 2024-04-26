"""Scree capture"""
from typing import Any

import numpy as np
from PIL import ImageGrab, Image
from numpy import ndarray, dtype


class ScreeCapture:
    capture: ndarray[Any, dtype[Any]]
    start_capture: ndarray[Any, dtype[Any]]

    main_color: ndarray[Any, dtype[Any]]
    white_color = np.array([255, 255, 255])
    black_color = np.array([0, 0, 0])

    @classmethod
    def get_cap(cls, point_left: int, point_top: int, point_right: int, point_bottom: int) -> None:
        """Captures the screen and returns the image obtained from the left-top and right-bottom points"""
        cls.start_capture = np.array(
            ImageGrab.grab(
                bbox=(point_left, point_top, point_right, point_bottom)
            )
        )
        cls.capture = np.array(
            ImageGrab.grab(
                bbox=(point_left, point_top, point_right, point_bottom)
            )
        )

        cls.segmentation()

    @classmethod
    def resize_xn(cls, img: Image, xn: int | list[int]) -> Image:
        if isinstance(xn, int):
            width = xn
            height = xn
        else:
            width = xn[0]
            height = xn[1]
        return img.resize((img.size[0] * width, img.size[1] * height))

    @classmethod
    def segmentation(cls):
        for line in range(cls.capture.shape[0]):
            for colum in range(cls.capture.shape[1]):
                if not np.array_equal(cls.capture[line][colum], cls.main_color):
                    cls.capture[line, colum] = cls.white_color
                else:
                    cls.capture[line, colum] = cls.black_color
