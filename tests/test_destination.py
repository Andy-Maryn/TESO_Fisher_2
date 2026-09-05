import pytest

from matrix.destination import Destination


class TestDestination:
    @pytest.mark.parametrize(
        'actual_destination_point, expected_destination', [
            pytest.param(0, (40.07, 84.28), id="0_point => (40.07, 84.28)"),
            pytest.param(7, (40.74, 81.7), id="7_point => (40.74, 81.7)")])
    def test_get_destination_point(self, actual_destination_point, expected_destination, load_data):
        Destination.current_destination = actual_destination_point
        assert Destination.get_destination_point() == expected_destination

    @pytest.mark.parametrize(
        'actual_destination_point', [
            pytest.param(0, id="0_point => [34.67, 45.23, 0]"),
            pytest.param(7, id="7_point => [27.67, 57.23, 1]")])
    def test_set_next_destination_point(self, actual_destination_point):
        Destination.current_destination = actual_destination_point
        Destination.set_next_destination_point()

        assert Destination.graph.adj[Destination.current_destination][actual_destination_point].get(
            'weight') == 2
