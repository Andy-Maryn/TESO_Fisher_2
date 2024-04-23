import math


class Moving:

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
