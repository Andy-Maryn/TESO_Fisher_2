from screenCapture.yet_another_compass_capture import CardinalDirections
from tests.common import *
from tests.conftest import base_image_array


class TestESOLocateCapture:
    @pytest.mark.requirement("FRS_TESO_FISHER_010103")
    @pytest.mark.parametrize(
        'eso_locate_capture, expected_location', [
            pytest.param(Path("4665_7969.jpeg"), (46.65, 79.69), id="4665_7969.jpeg => position: (46.65, 79.69)"),
            pytest.param(Path("4673_8010.jpeg"), (46.73, 80.10), id="4673_8010.jpeg => position: (46.83, 80.10)"),
            pytest.param(Path("4669_7987.jpeg"), (46.69, 79.87), id="4669_7987.jpeg => position: (56.69, 79.87)"),
            pytest.param(Path("4702_8082.jpeg"), (47.02, 80.82), id="4702_8082.jpeg => position: (47.02, 80.82)]"),
        ], indirect=['eso_locate_capture']
    )
    def test_get_current_position(self,
                                  eso_locate_capture: Path,
                                  expected_location: tuple[float, float],
                                  load_test_data,
                                  extras):
        extras.append(
            pytest_html.extras.image(
                base_image_array(ESOLocateCapture.capture, mode='1')
            )
        )
        actual_position = ESOLocateCapture.get_current_position()
        assert actual_position == expected_location


class TestYetAnotherCompassCapture:
    @pytest.mark.parametrize(
        'yet_another_compass_capture, expected_cardinal_direction', [
            pytest.param(Path("bottom_3.jpeg"), CardinalDirections.BOTTOM,
                         id="bottom_3.jpeg => cardinal_direction: BOTTOM"),
            pytest.param(Path("left_3.jpeg"), CardinalDirections.LEFT,
                         id="left_3.jpeg => cardinal_direction: LEFT"),
            pytest.param(Path("left_bottom_3.jpeg"), CardinalDirections.BOTTOM,
                         id="left_bottom_3.jpeg => cardinal_direction: BOTTOM"),
            pytest.param(Path("left_top_3.jpeg"), CardinalDirections.LEFT,
                         id="left_top_3.jpeg => cardinal_direction: LEFT"),
            pytest.param(Path("right_3.jpeg"), CardinalDirections.RIGHT,
                         id="right_3.jpeg => cardinal_direction: RIGHT"),
            pytest.param(Path("right_bottom_3.jpeg"), CardinalDirections.RIGHT,
                         id="right_bottom_3.jpeg => cardinal_direction: RIGHT"),
            pytest.param(Path("right_top_3.jpeg"), CardinalDirections.TOP,
                         id="right_top_3.jpeg => cardinal_direction: TOP"),
            pytest.param(Path("top_3.jpeg"), CardinalDirections.TOP,
                         id="top_3.jpeg => cardinal_direction: TOP"),
        ], indirect=['yet_another_compass_capture'])
    def test_get_compas_cardinal_directions(self,
                                            yet_another_compass_capture: Path,
                                            expected_cardinal_direction: CardinalDirections,
                                            load_test_data,
                                            extras):
        extras.append(
            pytest_html.extras.image(
                base_image_array(YetAnotherCompassCapture.capture, mode='1')
            )
        )
        actual_cardinal_direction = YetAnotherCompassCapture.get_cardinal_directions()
        assert actual_cardinal_direction == expected_cardinal_direction

    @pytest.mark.parametrize(
        'yet_another_compass_capture, expected_tip', [
            pytest.param(Path("bottom_3.jpeg"), (146, 76),
                         id="bottom_3.jpeg => tip: (146, 76)"),
            pytest.param(Path("left_3.jpeg"), (73, 3),
                         id="left_3.jpeg => tip: (73, 3)"),
            pytest.param(Path("left_bottom_3.jpeg"), (127, 26),
                         id="left_bottom_3.jpeg => tip: (127, 26)"),
            pytest.param(Path("left_top_3.jpeg"), (35, 16),
                         id="left_top_3.jpeg => tip: (35, 16)"),
            pytest.param(Path("right_3.jpeg"), (75, 146),
                         id="right_3.jpeg => tip: (75, 146)"),
            pytest.param(Path("right_bottom_3.jpeg"), (121, 128),
                         id="right_bottom_3.jpeg => tip: (121, 128)"),
            pytest.param(Path("right_top_3.jpeg"), (21, 122),
                         id="right_top_3.jpeg => tip: (21, 122)"),
            pytest.param(Path("top_3.jpeg"), (3, 73),
                         id="top_3.jpeg => tip: (3, 73)"),
        ], indirect=['yet_another_compass_capture'])
    def test_get_compas_tip(self,
                            yet_another_compass_capture: Path,
                            expected_tip: tuple[float, float],
                            load_test_data,
                            extras):
        extras.append(
            pytest_html.extras.image(
                base_image_array(YetAnotherCompassCapture.capture, mode='1')
            )
        )

        cardinal_direction = YetAnotherCompassCapture.get_cardinal_directions()
        actual_tip = YetAnotherCompassCapture.get_tip(cardinal_direction)
        assert actual_tip == expected_tip

    @pytest.mark.parametrize(
        'yet_another_compass_capture, expected_compas_direction', [
            pytest.param(Path("bottom_3.jpeg"), (1, 71),
                         id="bottom_3.jpeg => compas_direction: (1, 71)"),
            pytest.param(Path("left_3.jpeg"), (-72, -2),
                         id="left_3.jpeg => compas_direction: (-72, -2)"),
            pytest.param(Path("left_bottom_3.jpeg"), (-49, 52),
                         id="left_bottom_3.jpeg => compas_direction: (-49, 52)"),
            pytest.param(Path("left_top_3.jpeg"), (-59, -40),
                         id="left_top_3.jpeg => compas_direction: (-59, -40)"),
            pytest.param(Path("right_3.jpeg"), (71, 0),
                         id="right_3.jpeg => compas_direction: (71, 0)"),
            pytest.param(Path("right_bottom_3.jpeg"), (53, 46),
                         id="right_bottom_3.jpeg => compas_direction: (53, 46)"),
            pytest.param(Path("right_top_3.jpeg"), (47, -54),
                         id="right_top_3.jpeg => compas_direction: (47, -54)"),
            pytest.param(Path("top_3.jpeg"), (-2, -72),
                         id="top_3.jpeg => compas_direction: (-2, -72)"),
        ], indirect=['yet_another_compass_capture'])
    def test_get_compas_direction(self,
                                  yet_another_compass_capture: Path,
                                  expected_compas_direction: tuple[float, float],
                                  load_test_data,
                                  extras):
        extras.append(
            pytest_html.extras.image(
                base_image_array(YetAnotherCompassCapture.capture, mode='1')
            )
        )
        cardinal_direction = YetAnotherCompassCapture.get_cardinal_directions()
        tip = YetAnotherCompassCapture.get_tip(cardinal_direction)
        actual_compas_direction = YetAnotherCompassCapture.get_compas_direction(tip)
        assert actual_compas_direction == expected_compas_direction

    # def test_get_compas_direction_(self, load_data):
    #     time.sleep(3)
    #     YetAnotherCompassCapture.get_cap()
    #
    #     current_time = time.time()
    #     folder = time.strftime(f"%Y%m%d_%H%M%S_{round(current_time * 1000)}", time.gmtime(current_time))
    #     os.makedirs(f"report/{folder}")
    #
    #     Image.fromarray(YetAnotherCompassCapture.start_capture).save(
    #         os.path.dirname(os.path.abspath(__file__)) + f"/report/{folder}/compas.jpeg")
