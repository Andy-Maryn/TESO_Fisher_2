import logging
import math
import time
from typing import Callable

import mouse

from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture

logger = logging.getLogger('rotation.py')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


class Rotation:
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

    __p2d: Callable[[float], float] = lambda x: ((x - abs(x) / x) / 0.144) + 0.15
    # __d2p: Callable[[float], float] = lambda y: (y - 0.15) * 0.144 + (abs(y) / y)
    __d2p: Callable[[float], float] = lambda y: (y - 7.1 * (abs(y) / y)) / 6.9 if y != 0 else 0

    # __d2p: Callable[[float], float] = lambda y: y / 0.144

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

        get_degree: Callable[[float, float], float] = lambda _x, _y: math.degrees(math.atan(_y / _x))

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
    def calibration(degree: float) -> float:
        """
            90 60 30                    (60+180) 240
            -30 +30

            45 15 360-15 (345)
            -30
        :param degree:
        :return:
        """

        logger.info(f"-get_compas_direction: {YetAnotherCompassCapture.get_compas_direction()}")
        compas_degree = Rotation.get_degree((0, 0), (YetAnotherCompassCapture.get_compas_direction()))

        logger.info(f"-compas_degree: {compas_degree}")
        logger.info(f"-degree: {degree}")
        move = Rotation._calibrate(degree, compas_degree)
        logger.info(f"-move_that_we_take: {move}")

        logger.info(f"-Rotation: {Rotation.__d2p(move)}")
        # Rotation.move_mouse(Rotation.__d2p(move))
        return move


if __name__ == "__main__":
    YetAnotherCompassParser.load_data()
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
    YetAnotherCompassCapture.get_cap()
    compas_direction = YetAnotherCompassCapture.get_compas_direction()
    degree_1 = Rotation.get_degree(start_point=(0, 0), destination_point=tuple(compas_direction))
    print("degree: ", degree_1)

    for i in range(20):
        print(f'-{i}___')
        Rotation.move_mouse(i, 0, 1)
        YetAnotherCompassCapture.get_cap()
        compas_direction = YetAnotherCompassCapture.get_compas_direction()
        degree_2 = Rotation.get_degree(start_point=(0, 0), destination_point=tuple(compas_direction))
        print("degree: ", degree_2)
        print("degree_1 - degree_2", degree_1 - degree_2)
        degree_1 = degree_2
