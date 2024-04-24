import numpy as np

#                            0  1  2  3  4  5  6  7
map_destination = np.array([[0, 1, 1, 0, 0, 0, 0, 0],  # 0
                            [1, 0, 1, 1, 0, 0, 0, 1],  # 1
                            [1, 1, 0, 0, 1, 0, 0, 1],  # 2
                            [0, 1, 0, 0, 0, 1, 0, 0],  # 3
                            [0, 0, 1, 0, 0, 1, 0, 0],  # 4
                            [0, 0, 0, 1, 1, 0, 1, 0],  # 5
                            [0, 0, 0, 0, 0, 1, 0, 0],  # 6
                            [0, 7, 1, 0, 0, 0, 0, 0]])  # 7

if __name__ == "__main__":
    np.save('adjacency_matrix.npy', map_destination)  # .npy extension is added if not given
