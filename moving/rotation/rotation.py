import math
import time
from typing import Callable

import mouse

from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture


class Rotation:
    a = 1
    degree: Callable[[float], float] = lambda x: math.degrees(
        math.atan(
            math.tan(
                math.radians(
                    (x + 180) / 2
                )
            )
        )
    ) * 2 + 180
    calibrate: Callable[[float], float] = lambda x, a: math.degrees(
        math.atan(
            math.tan(
                math.radians(
                    (-x + a) / 2
                )
            )
        )
    ) * 2
    __p2d: Callable[[float], float] = lambda x: ((x - abs(x) / x) / 0.144) + 0.15
    __d2p: Callable[[float], float] = lambda y: (y - 0.15) * 0.144 + abs(y) / y

    # TODO: setup duration
    @staticmethod
    def move_mouse(x: int, y: int = 0, duration: float = 0.2):
        mouse.move(x=x,
                   y=y,
                   absolute=False,
                   duration=duration)

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

        return Rotation.degree(degree)

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
        current_degree = Rotation.get_degree((0, 0), (YetAnotherCompassCapture.get_compas_direction()))
        return Rotation.calibrate(degree, current_degree)
        # Rotation.move_mouse(Rotation.__d2p(move))


if __name__ == "__main__":
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

    Rotation.move_mouse(10, 0, 0.5)
    # Rotation.move_mouse(-10, 0, 1)
