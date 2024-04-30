from tests.common import *


class TestESOLocateCapture:
    @pytest.mark.parametrize(
        'eso_locate_capture, expected_location', [
            pytest.param(Path("4715_8270.jpeg"), [47.15, 82.70]),
            pytest.param(Path("4719_8287.jpeg"), [47.19, 82.87]),
        ], indirect=['eso_locate_capture']
    )
    def test_eso_locate_get_current_position(self, eso_locate_capture, expected_location):
        actual_position = ESOLocateCapture.get_current_position()
        assert actual_position == expected_location


class TestYetAnotherCompassCapture:
    @pytest.mark.parametrize(
        'yet_another_compass_capture, expected_location', [
            pytest.param(Path("4730_8228.jpeg"), (-21, 55)),
            pytest.param(Path("4739_8325.jpeg"), (32, 39)),
            pytest.param(Path("4777_8315.jpeg"), (49, -18)),
        ], indirect=['yet_another_compass_capture']
    )
    def test_eso_locate_get_compas_direction(self, yet_another_compass_capture, expected_location):

        actual_position = YetAnotherCompassCapture.get_compas_direction()
        assert actual_position == expected_location
