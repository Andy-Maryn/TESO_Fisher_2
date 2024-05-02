import random
from pathlib import Path

import networkx as nx
import numpy as np


class Destination:
    _root: Path = Path(r'C:\Users\Andy\PycharmProjects\tesoFisher\matrix')
    file_name: str = 'adjacency_matrix.npz'

    @classmethod
    @property
    def path(cls) -> Path:
        return cls._root / cls.file_name

    destination_points: np.array
    adjacency_matrix: np.array

    graph: nx.DiGraph

    current_destination: int = 0

    @classmethod
    def load_data(cls) -> None:

        cls.destination_points = np.load(cls.path)['destination_points']
        cls.adjacency_matrix = np.load(cls.path)['map_destination']

        cls.graph = nx.DiGraph(np.matrix(cls.adjacency_matrix))

    @classmethod
    def get_destination_point(cls):
        return cls.destination_points[cls.current_destination]

    @classmethod
    def set_next_destination_point(cls):
        destination_point: dict = cls.graph.adj[cls.current_destination]
        weights = [weight['weight'] for key, weight in destination_point.items()]
        min_weight = min(weights)
        weights_count = weights.count(min_weight)
        number = 1
        if weights_count > 1:
            number = random.SystemRandom().randint(1, weights_count)
        next_destination_point_key = [i for i in destination_point.keys()][0]
        for key, value in destination_point.items():
            if value['weight'] == min_weight:
                if number == 1:
                    next_destination_point_key = key
                else:
                    number -= 1

        cls.graph.adj[next_destination_point_key][cls.current_destination]['weight'] += 1

        cls.current_destination = next_destination_point_key
