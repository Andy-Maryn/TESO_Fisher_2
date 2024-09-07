from luaParser.eso_locate_parser import ESOLocateParser
from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from matrix.destination import Destination
from moving.rotation.rotation import Rotation
from screenCapture.eso_locate_capture import ESOLocateCapture
from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture

ESOLocateParser.load_data()
ESOLocateParser.set_user_property('BendreTolstyy')
YetAnotherCompassParser.load_data()
Destination.load_data()

current_position = ESOLocateCapture.get_current_position()
destination_point = Destination.get_destination_point()

degree = Rotation.get_degree(current_position, destination_point)

cardinal_direction = YetAnotherCompassCapture.get_cardinal_directions()
tip = YetAnotherCompassCapture.get_tip(cardinal_direction)
compas_degree = Rotation.get_degree((0, 0), (YetAnotherCompassCapture.get_compas_direction(tip)))

calibration = Rotation._calibrate(degree, compas_degree)
Rotation.move_mouse(calibration)
