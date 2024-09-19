"""Scree capture"""
from pathlib import Path
from typing import Any

import numpy as np
from PIL import ImageGrab, Image
from numpy import ndarray, dtype

from definitions import ROOT_DIR

ROOT: Path = ROOT_DIR


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

        # cls.segmentation()

    @classmethod
    def resize_xn(cls, img: Image, xn: int | list[int]) -> Image:
        if isinstance(xn, int):
            width = xn
            height = xn
        else:
            width = xn[0]
            height = xn[1]
        return img.resize((img.size[0] * width, img.size[1] * height))

    '''
    @classmethod
    def segmentation(cls):
        new_capture = np.zeros((cls.capture.shape[0], cls.capture.shape[1]))
        for line in range(cls.capture.shape[0]):
            for colum in range(cls.capture.shape[1]):
                if np.array_equal(cls.capture[line][colum], cls.main_color):
                    new_capture[line, colum] = 1
        cls.capture = new_capture
    '''

    @classmethod
    def segmentation(cls, color_error: int = 1):
        new_capture = np.zeros((cls.capture.shape[0], cls.capture.shape[1]))
        for line in range(cls.capture.shape[0]):
            for colum in range(cls.capture.shape[1]):
                if cls.capture[line][colum][0] in range(cls.main_color[0] - color_error,
                                                        cls.main_color[0] + color_error) and \
                        cls.capture[line][colum][1] in range(cls.main_color[1] - color_error,
                                                             cls.main_color[1] + color_error) and \
                        cls.capture[line][colum][2] in range(cls.main_color[2] - color_error,
                                                             cls.main_color[2] + color_error):
                    new_capture[line, colum] = 1
        cls.capture = new_capture
