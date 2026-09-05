import time

import pytest
from pytest_check import check

from common import logger
from fisherman.fisherman import Fisherman
from moving.gps import Gps
from moving.rotation.rotation import Rotation
from moving.walking import Walking
from tests.conftest import TESO_RUNNING


class TestMoving:
    @pytest.mark.skipif(TESO_RUNNING is not True, reason="'eso64.exe' is not running")
    def test_moving_to_point(self, load_data, screen_is_ready, mouse_sensitivity):
        step = 0.2
        # points = [(current_position[0] + step, current_position[1] + step),
        #           (current_position[0] + step, current_position[1] - step),
        #           (current_position[0] - step, current_position[1] - step),
        #           (current_position[0] - step, current_position[1] + step)]
        #
        # for destination_point in points:

        #  Set current_position
        Fisherman.set_current_position()
        logger.info(f"-current_position: {Gps.current_position}")

        #  Set destination_point
        destination_point = (Gps.current_position[0] + step, Gps.current_position[1] + step)
        Fisherman.set_destination_point(destination_point)
        logger.info(f"-destination_point: {Gps.current_destination}")

        #  Calibrate direction of view
        calibration = Fisherman.direction_of_view()
        logger.info(f"-calibration: {calibration}")

        with check:
            assert -5 < Rotation.p2d(calibration) < 5, 'Wrong calibration result'

        #  Calculate distance between points
        previous_distance = Gps.get_distance()
        logger.info(f"-start_distance: {previous_distance}")

        start_time = time.time()
        while Gps.is_it_destination_point(0.15) is not True and time.time() - start_time < 50:
            # Start/Continue walking
            Walking.start()
            logger.info(f"-start_Walking")

            #  Set current_position
            Fisherman.set_current_position()
            logger.info(f"-current_position -> destination_point: {Gps.current_position} -> {Gps.current_destination}")

            #  Calculate distance between points
            current_distance = Gps.get_distance()
            logger.info(f"-current_distance: {current_distance}")
            logger.info(f"-previous_distance: {previous_distance}")

            while current_distance < previous_distance and time.time() - start_time < 50:
                #  Set current_position
                Fisherman.set_current_position()
                logger.info(f"-current_position: {Gps.current_position}")
                logger.info(f"-destination_point: {Gps.current_destination}")

                #  Calculate distance between points
                previous_distance = current_distance
                current_distance = Gps.get_distance()

                logger.info(f"-current_distance: {current_distance}")
                logger.info(f"-previous_distance: {previous_distance}")

            Walking.stop()
            logger.info(f"-stop_Walking")
            Fisherman.direction_of_view(Gps.current_position, destination_point)

        Walking.stop()
        assert Gps.is_it_destination_point(0.15), 'Arrival point reached / Can not reach the destination'
