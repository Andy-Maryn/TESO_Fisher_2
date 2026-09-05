import math
import time

import numpy as np
from PIL import Image

from common import logger
from screenCapture.coords_and_heading_capture.coords_and_heading_capture import CoordsAndHeadingCapture


class Gps:
    current_position: tuple[float, float] = None
    current_destination: tuple[float, float] = None

    error = 0.05

    @classmethod
    def get_current_position(cls, wait: int = 0) -> tuple[float, float]:
        start_time = time.time()

        def get_position(current_time: float = time.time()):
            if current_time - start_time < wait:
                # Get image screen
                CoordsAndHeadingCapture.get_cap()

                # Try to get current position
                current_position = CoordsAndHeadingCapture.get_numbers()[:2]

                return current_position if current_position is not None else get_position(time.time())
            else:
                return None

        cls.current_position = get_position()

        return cls.current_position

    # @classmethod
    # def verify_current_position(cls, start_point: tuple[float, float]):
    #     if cls.current_destination is not None:
    #         verify = [False, False]
    #         for i in range(2):
    #             bord_value = [start_point[i], cls.current_destination[i]]
    #             if min(bord_value) - cls.error <= cls.current_position[i] <= max(bord_value) + cls.error:
    #                 verify[i] = True
    #     else:
    #         verify = [True, True]
    #     return all(verify) is True
    @classmethod
    def get_distance(cls):
        return math.hypot(cls.current_destination[0] - cls.current_position[0],
                          cls.current_destination[1] - cls.current_position[1])

    @classmethod
    def is_it_destination_point(cls, d =  0.05):
        distance = cls.get_distance()
        logger.info(f"-distance: {distance}")
        return distance < d


if __name__ == "__main__":
    with Image.open(
            r'C:\Users\Andrii\PycharmProjects\pyWinCoreAudio\report\20240425_211350_1714079630810\locate_.jpeg') as file:
        CoordsAndHeadingCapture.capture = np.asarray(file)

        position = CoordsAndHeadingCapture.get_numbers()[:2]
        print(position)
