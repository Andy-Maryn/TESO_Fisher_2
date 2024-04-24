import math
import random
import time

import mouse


class Moving:

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

        print(x, y)

        degree = math.degrees(math.atan(y / x))
        print(degree)

        if x > 0:
            degree = cycle - ((cycle / 4) - degree)
        elif x < 0:
            degree = (cycle / 4) + degree
        else:
            if y > 0:
                degree = 0
            else:
                degree = 180

        return degree


if __name__ == "__main__":
    time.sleep(3)
    duration = random.SystemRandom().uniform(0.1, 1)
    Moving.move_mouse(100, 0, duration)

    duration = random.SystemRandom().uniform(0.1, 1)
    Moving.move_mouse(100, 0, duration)

    duration = random.SystemRandom().uniform(0.1, 1)
    Moving.move_mouse(100, 0, duration)

    duration = random.SystemRandom().uniform(0.1, 1)
    Moving.move_mouse(100, 0, duration)
