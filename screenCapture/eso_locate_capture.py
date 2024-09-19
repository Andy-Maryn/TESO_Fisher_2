"""ESOLocate capture"""
import json
import re

from luaParser.eso_locate_parser import ESOLocateParser
from screenCapture.screen_capture import *


# PATTERN = r"\d{2,3}[.,]\d{2}.*?\d{2,3}[.,]\d{2}\n"


class ESOLocateCapture(ScreeCapture):
    """Captures an image of ESOLocate coordinates"""
    # main_color = np.array([207, 220, 189])
    main_color = np.array([0, 0, 0])

    _digit_size = 8
    _sign_size = 4
    _space_size = 8
    convert_format: str = '00.00 00.00'
    convert_format_digit = []
    with open(ROOT / r"screenCapture\eso_locate_masks.json", mode="r",
              encoding="utf-8") as file:
        _digits: dict[str, int] = json.load(file)

    __val = 0
    for i in convert_format:
        if i.isdigit():
            __val += _digit_size
            convert_format_digit.append(__val)
        elif i.isspace():
            __val += _space_size
            convert_format_digit.append(__val)
        else:
            __val += _sign_size
            convert_format_digit.append(__val)

    @classmethod
    def get_cap(cls, **kwargs) -> ndarray[Any, dtype[Any]]:
        super().get_cap(
            point_left=ESOLocateParser.left_point,
            point_top=ESOLocateParser.top_point,
            point_right=ESOLocateParser.right_point,
            point_bottom=ESOLocateParser.bottom_point)

        cls.capture = cls.capture[5:18, 110:190]
        return cls.capture

    @classmethod
    def get_separate_data(cls):
        """
        Splits a coordinate image into individual numbers
        :return:
        """
        return np.split(cls.capture, [8, 16, 20, 28, 36, 44, 52, 60, 64, 72, 80], axis=1)

    @classmethod
    def __convert_ndarray_2_text(cls) -> str:
        digit_matrix_list = np.split(cls.capture, cls.convert_format_digit, axis=1)
        result = ''
        for digit_matrix in digit_matrix_list:
            if digit_matrix.shape[1] == cls._sign_size:
                result = result + '.'
                continue
            elif digit_matrix.shape[1] == cls._digit_size:
                _current_rel = 0
                sign = ''
                for key, digit in cls._digits.items():
                    digit = np.array(digit)
                    digit_matrix = digit_matrix.astype(int)
                    _rel = np.sum(
                        ((~digit_matrix & ~digit) | (digit_matrix & digit)) + 2
                    )
                    if _rel > 100:
                        sign = key
                        break
                    elif _rel > _current_rel:
                        _current_rel = _rel
                        sign = key
            else:
                continue
            result = result + sign
        return result

    @classmethod
    def get_current_position(cls) -> tuple[float, float]:
        """
        Return current position
        :return:
        """
        string = cls.__convert_ndarray_2_text()
        coordinates: list[float] = []
        coord_list = re.findall(r'\d{2,3}[.,]\d\d', string)
        for coord in coord_list:
            coordinates.append(
                float(
                    coord.replace(',', '.')
                )
            )
        return tuple(coordinates)
