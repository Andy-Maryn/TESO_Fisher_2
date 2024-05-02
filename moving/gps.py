import time

import numpy as np
from PIL import Image

from screenCapture.eso_locate_capture import ESOLocateCapture


class Gps:
    current_position: tuple[float, float]

    @classmethod
    def get_current_position(cls, wait: int = 5) -> tuple[float, float]:
        start_time = time.time()

        def get_position(current_time: float = time.time()):
            if current_time - start_time < wait:
                # Get image screen
                ESOLocateCapture.get_cap()

                # Try to get current position
                current_position = ESOLocateCapture.get_current_position()

                return current_position if current_position is not None else cls.get_current_position()
            else:
                return None

        cls.current_position = get_position()

        return cls.current_position

    @classmethod
    def verify_current_position(cls, start_point: tuple[float, float], destination_point: tuple[float, float]):
        verify = [False, False]
        for i in range(2):
            bord_value = [start_point[i], destination_point[i]]
            if min(bord_value) - 1 <= cls.current_position[i] <= max(bord_value) + 1:
                verify[i] = True
        return all(verify) is True

    @classmethod
    def is_it_destination_point(cls, destination_point: tuple[float, float]):
        verify = [False, False]
        for i in range(2):
            if destination_point[i] - 1 <= cls.current_position[i] <= destination_point[i] + 1:
                verify[i] = True
        return all(verify) is True


if __name__ == "__main__":
    with Image.open(
            r'C:\Users\Andy\PycharmProjects\pyWinCoreAudio\report\20240425_211350_1714079630810\locate_.jpeg') as file:
        ESOLocateCapture.capture = np.asarray(file)

        position = ESOLocateCapture.get_current_position()
        print(position)
