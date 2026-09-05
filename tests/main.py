from luaParser.coords_and_heading_parser.coords_and_heading_parser import CoordsAndHeadingParser
from matrix.destination import Destination
from moving.rotation.rotation import Rotation

CoordsAndHeadingParser.load_data()
Destination.load_data()

current_position = CoordsAndHeadingCapture.get_current_position()
destination_point = Destination.get_destination_point()

degree = Rotation.get_degree(current_position, destination_point)

cardinal_direction = YetAnotherCompassCapture.get_cardinal_directions()
tip = YetAnotherCompassCapture.get_tip(cardinal_direction)
compas_degree = Rotation_get_degree((0, 0), (YetAnotherCompassCapture.get_compas_direction(tip)))

calibration = Rotation._calibrate(degree, compas_degree)
Rotation.move_mouse(calibration)
