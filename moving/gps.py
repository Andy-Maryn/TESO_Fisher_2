import logging
import math
import time

import numpy as np
from PIL import Image

from screenCapture.eso_locate_capture import ESOLocateCapture

logger = logging.getLogger('gps.py')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)
class Gps:
    current_position: tuple[float, float]

    error = 0.05

    @classmethod
    def get_current_position(cls, wait: int = 8) -> tuple[float, float]:
        start_time = time.time()

        def get_position(current_time: float = time.time()):
            if current_time - start_time < wait:
                # Get image screen
                ESOLocateCapture.get_cap()

                # Try to get current position
                current_position = ESOLocateCapture.get_current_position()

                return current_position if current_position is not None else get_position(time.time())
            else:
                return None

        cls.current_position = get_position()

        return cls.current_position

    @classmethod
    def verify_current_position(cls, start_point: tuple[float, float], destination_point: tuple[float, float]):
        verify = [False, False]
        for i in range(2):
            bord_value = [start_point[i], destination_point[i]]
            if min(bord_value) - cls.error <= cls.current_position[i] <= max(bord_value) + cls.error:
                verify[i] = True
        return all(verify) is True

    @classmethod
    def is_it_destination_point(cls, destination_point: tuple[float, float]):
        distance = math.hypot(destination_point[0] - cls.current_position[0],
                              destination_point[1] - cls.current_position[1])
        logger.info(f"-distance: {distance}")
        return distance < 0.5


if __name__ == "__main__":
    with Image.open(
            r'C:\Users\Andy\PycharmProjects\pyWinCoreAudio\report\20240425_211350_1714079630810\locate_.jpeg') as file:
        ESOLocateCapture.capture = np.asarray(file)

        position = ESOLocateCapture.get_current_position()
        print(position)
