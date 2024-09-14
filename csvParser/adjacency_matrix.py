from pathlib import Path
from typing import Optional

from csvParser.csv_parser import CsvParser
from definitions import ROOT_DIR


class AdjacencyMatrixParser(CsvParser):
    """AdjacencyMatrix Parser"""
    _root: Path = ROOT_DIR / 'matrix'
    csv_file_name: str = 'adjacency_matrix.csv'

    destination_points: Optional[dict[int, tuple[float, float]]] = None
    map_destination: Optional[list[int,int]] = None
    is_destination: Optional[dict[int, float]] = None

    @classmethod
    @property
    def path(cls) -> Path:
        return cls._root / cls.csv_file_name

    @classmethod
    def load_data(cls) -> None:
        super(AdjacencyMatrixParser, cls).load_data()
        cls.set_destination_points()

    @classmethod
    def set_destination_points(cls) -> None:
        cls.destination_points = {}
        cls.map_destination = []
        cls.is_destination = {}
        for row in cls.load_list[1:]:
            point_count = len(row)-3
            map_destination = []
            index: int = int(row.get('index'))
            destination_point: tuple[float, float] = eval(row.get('destination_point'))
            is_destination: float = True if row.get('isDestination') else False
            for i in range(point_count):
                map_destination.append(int(row.get(str(i))))
            cls.destination_points.update({index: destination_point})
            cls.is_destination.update({index: is_destination})
            cls.map_destination.append(map_destination)
