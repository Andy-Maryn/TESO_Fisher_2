"""ESOLocate capture"""
import dataclasses
import re

import numpy as np
import pytesseract
from PIL import Image

from luaParser.eso_locate_parser import ESOLocateParser
from screenCapture.screen_capture import ScreeCapture

PATTERN = r"\d{2,3}[.,]\d{2}.*?\d{2,3}[.,]\d{2}\n"


class ESOLocateCapture(ScreeCapture):
    """Captures an image of ESOLocate coordinates"""
    main_color = np.array([207, 220, 189])

    @classmethod
    def get_cap(cls, **kwargs):
        super().get_cap(
            point_left=ESOLocateParser.left_point,
            point_top=ESOLocateParser.top_point,
            point_right=ESOLocateParser.right_point,
            point_bottom=ESOLocateParser.bottom_point)

        cls.capture = cls.capture[:, 110:190, :]

    @classmethod
    def get_separate_data(cls):
        """
        Splits a coordinate image into individual numbers
        :return:
        """
        return np.split(cls.capture, [8, 16, 20, 28, 36, 44, 52, 60, 64, 72, 80], axis=1)

    @classmethod
    def __convert_image_2_text(cls) -> str:
        return pytesseract.image_to_string(cls.resize_xn(
            Image.fromarray(
                obj=cls.capture,
                mode='RGB'
            ), [3, 3]
        ), config='r-l equ')

    @classmethod
    def get_current_position(cls) -> list[float] | None:
        """
        Return current position
        :return:
        """
        string = cls.__convert_image_2_text()
        coordinates: list[float] = []
        if re.fullmatch(pattern=PATTERN, string=string):
            coord_list = re.findall(r'\d{2,3}[.,]\d\d', string)
            for coord in coord_list:
                coordinates.append(
                    float(
                        coord.replace(',', '.')
                    )
                )
            return coordinates
        else:
            return None
