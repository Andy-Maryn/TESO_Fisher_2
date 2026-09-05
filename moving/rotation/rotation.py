import math
import time
from typing import Callable

import mouse
import numpy as np

from common import logger
from luaParser.coords_and_heading_parser.coords_and_heading_parser import CoordsAndHeadingParser
from screenCapture.coords_and_heading_capture.coords_and_heading_capture import CoordsAndHeadingCapture


class Rotation:
    m = 2.825
    b = -2.795

    a = 1
    _degree: Callable[[float], float] = lambda x: math.degrees(
        math.atan(
            math.tan(
                math.radians(
                    (x + 180) / 2
                )
            )
        )
    ) * 2 + 180
    # _calibrate: Callable[[float], float] = lambda x, a: math.degrees(
    #     math.atan(
    #         math.tan(
    #             math.radians(
    #                 (-x + a) / 2
    #             )
    #         )
    #     )
    # ) * 2

    x_invert_degree: Callable[[float], float] = lambda x: 180 - x

    __calibrate: Callable[[float], float] = lambda x: math.degrees(
        math.atan(
            math.tan(
                math.radians(
                    x / 2
                )
            )
        )
    ) * 2
    _calibrate: Callable[[float], float] = lambda degree, compas_degree: Rotation.__calibrate(
        compas_degree - degree
    )

    p2d: Callable[[float], float] = lambda x: (Rotation.m * x) + Rotation.b
    _d2p: Callable[[float], float] = lambda y: (y - Rotation.b) / Rotation.m

    @classmethod
    def mouse_sensitivity(cls, x, y):
        _a = np.vstack([x, np.ones(len(x))]).T
        cls.m, cls.b = np.linalg.lstsq(_a, y, rcond=None)[0]
        time.sleep(0.5)
        logger.info(f"m = {cls.m},  b = {cls.b}")

    @classmethod
    def calculate_mouse_sensitivity(cls):
        _x = []
        _y = []

        CoordsAndHeadingCapture.get_cap()
        CoordsAndHeadingCapture.segmentation(20)
        start_compas_degree = CoordsAndHeadingCapture.get_heading().camera_heading

        for move in range(1, 30, 1):
            cls.move_mouse(move)

            CoordsAndHeadingCapture.get_cap()
            CoordsAndHeadingCapture.segmentation(20)
            new_compas_degree = CoordsAndHeadingCapture.get_heading().camera_heading

            degree = abs(new_compas_degree - start_compas_degree)

            logger.info(f"degree = {degree}")

            if 1 < degree < 180:
                logger.info(f"_x = {move},  _y = {degree}")
                _x.append(move)
                _y.append(degree)
            start_compas_degree = new_compas_degree

        cls.mouse_sensitivity(_x, _y)

    # TODO: setup duration
    @staticmethod
    def move_mouse(x: int, y: int = 0, duration: float = 0.2):
        mouse.move(x=x,
                   y=y,
                   absolute=False,
                   duration=Rotation.a)

    @staticmethod
    def get_degree(start_point: tuple[float, float], destination_point: tuple[float, float]) -> float:
        cycle = 360

        _x, _y = start_point
        x, y = destination_point
        x -= _x
        y -= _y

        get_degree: Callable[[float, float], float] = lambda __x, __y: math.degrees(math.atan(__y / __x))

        if x > 0:
            degree = get_degree(x, y)
        elif x < 0:
            degree = (cycle / 2) + get_degree(x, y)
        else:
            if y > 0:
                degree = 90
            else:
                degree = 270

        return Rotation._degree(degree)

    @staticmethod
    def calibration(degree: float, compas_degree: float) -> int:
        """
            90 60 30                    (60+180) 240
            -30 +30

            45 15 360-15 (345)
            -30
        :param degree:
        :return:
        """
        move = Rotation._calibrate(degree, compas_degree)
        logger.info(f"-move_that_we_take: {move}")
        return Rotation._d2p(move)


if __name__ == "__main__":
    CoordsAndHeadingParser.load_data()
    time.sleep(3)
    # _duration = random.SystemRandom().uniform(0.1, 1)
    # print(_duration)
    # Rotation.move_mouse(10, 0, _duration)
    #
    # _duration = random.SystemRandom().uniform(0.1, 1)
    # print(_duration)
    # Rotation.move_mouse(-10, 0, _duration)
    #
    # _duration = random.SystemRandom().uniform(0.1, 1)
    # print(_duration)
    # Rotation.move_mouse(10, 0, _duration)
    #
    # _duration = random.SystemRandom().uniform(0.1, 1)
    # print(_duration)
    # Rotation.move_mouse(-10, 0, _duration)

    # Rotation.move_mouse(10, 0, 0.5)
    # Rotation.move_mouse(-10, 0, 1)
    CoordsAndHeadingCapture.get_cap()
    degree_1 = CoordsAndHeadingCapture.get_heading().camera_heading
    print("degree: ", degree_1)

    for i in range(20):
        print(f'-{i}___')
        Rotation.move_mouse(i, 0, 1)
        CoordsAndHeadingCapture.get_cap()
        degree_2 = CoordsAndHeadingCapture.get_heading().camera_heading
        print("degree: ", degree_2)
        print("degree_1 - degree_2", degree_1 - degree_2)
        degree_1 = degree_2
