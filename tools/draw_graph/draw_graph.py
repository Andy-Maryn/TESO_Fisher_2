import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    adjacency_matrix = np.load('adjacency_matrix.npy')

    G = nx.DiGraph(np.matrix(adjacency_matrix))
    pos = nx.bfs_layout(G, 0)
    nx.draw(G, pos, with_labels=True, node_size=300, arrows=True)
    plt.show()
