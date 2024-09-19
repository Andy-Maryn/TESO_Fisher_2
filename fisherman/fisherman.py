from matrix.destination import Destination
from moving.gps import Gps
from moving.rotation.rotation import Rotation
from screenCapture.eso_locate_capture import ESOLocateCapture
from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture


class Fisherman:
    @staticmethod
    def set_current_position(current_position: tuple[float, float] = None):
        current_position = current_position if current_position is not None else Fisherman.update_current_position()
        Gps.current_position = current_position

    @staticmethod
    def set_destination_point(destination_point: tuple[float, float] = None):
        destination_point = destination_point if destination_point is not None else Destination.get_destination_point()
        Gps.current_destination = destination_point

    @staticmethod
    def update_current_position() -> tuple[float, float]:
        ESOLocateCapture.get_cap()
        ESOLocateCapture.segmentation()

        return ESOLocateCapture.get_current_position()

    @staticmethod
    def update_current_compas_direction() -> float:
        YetAnotherCompassCapture.get_cap()
        YetAnotherCompassCapture.segmentation()

        cardinal_direction = YetAnotherCompassCapture.get_cardinal_directions()
        tip = YetAnotherCompassCapture.get_tip(cardinal_direction)
        compas_direction = YetAnotherCompassCapture.get_compas_direction(tip)

        return Rotation.get_degree((0, 0), compas_direction)

    @staticmethod
    def direction_of_view(current_point: tuple[float, float] = None,
                          destination_point: tuple[float, float] = None):
        current_position = Gps.current_position if current_point is None else current_point
        destination_point = Gps.current_destination if destination_point is None else destination_point

        degree = Rotation.get_degree(current_position, destination_point)
        degree = Rotation.x_invert_degree(degree)

        compas_degree = Fisherman.update_current_compas_direction()
        calibration = Rotation.calibration(degree, compas_degree)
        Rotation.move_mouse(calibration)

        compas_degree = Fisherman.update_current_compas_direction()
        calibration = Rotation.calibration(degree, compas_degree)

        if -5 > Rotation.p2d(calibration) > 5:
            Rotation.move_mouse(calibration)
        return calibration
