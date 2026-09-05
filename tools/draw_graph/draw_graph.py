import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from definitions import ROOT_DIR

if __name__ == "__main__":
    path = ROOT_DIR + 'tools/draw_graph/adjacency_matrix.csv'
    with open(path, "r", encoding="utf8") as file:
        destination_points = file.read()

    destination_points = np.load(ROOT_DIR + 'tools/draw_graph/adjacency_matrix.csv')['destination_points']
    adjacency_matrix = np.load(ROOT_DIR + 'tools/draw_graph/adjacency_matrix.csv')['map_destination']

    G = nx.DiGraph(np.matrix(adjacency_matrix))
    pos = nx.bfs_layout(G, 0)
    nx.draw(G, pos, with_labels=True, node_size=300, arrows=True)
    print(G.adj[2])
    plt.show()
