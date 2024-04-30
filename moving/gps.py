import time

import numpy as np
from PIL import Image

from screenCapture.eso_locate_capture import ESOLocateCapture


class Gps:

    @classmethod
    def get_current_position(cls, wait: int = 5):
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

        return get_position()

    @classmethod
    def step_get_degree_between_current_and_destination_points(cls):
        pass


if __name__ == "__main__":
    with Image.open(
            r'C:\Users\Andy\PycharmProjects\pyWinCoreAudio\report\20240425_211350_1714079630810\locate_.jpeg') as file:
        ESOLocateCapture.capture = np.asarray(file)

        position = ESOLocateCapture.get_current_position()
        print(position)
