import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    destination_points = np.load('../../tools/draw_graph/adjacency_matrix.npz')['destination_points']
    adjacency_matrix = np.load('../../tools/draw_graph/adjacency_matrix.npz')['map_destination']

    G = nx.DiGraph(np.matrix(adjacency_matrix))
    pos = nx.bfs_layout(G, 0)
    nx.draw(G, pos, with_labels=True, node_size=300, arrows=True)
    print(G.adj[2])
    plt.show()
