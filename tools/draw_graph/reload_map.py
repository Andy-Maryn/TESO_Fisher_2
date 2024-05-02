import numpy as np

#                            0  1  2  3  4  5  6  7
map_destination = np.array([[0, 1, 0, 0, 0, 0, 0, 0],  # 0
                            [1, 0, 1, 0, 0, 0, 0, 0],  # 1
                            [0, 1, 0, 1, 0, 0, 0, 0],  # 1
                            [0, 0, 1, 0, 1, 0, 0, 0],  # 1
                            [0, 0, 0, 1, 0, 1, 0, 0],  # 1
                            [0, 0, 0, 0, 1, 0, 1, 0],  # 1
                            [0, 0, 0, 0, 0, 1, 0, 1],  # 1
                            [0, 0, 0, 0, 0, 0, 1, 0]])  # 7

destination_points = np.array(
    [[40.07, 84.28, 0],  # 0
     [40.47, 83.78, 0],  # 1
     [39.98, 83.39, 0],  # 2
     [39.73, 83.09, 1],  # 3
     [40.12, 82.89, 0],  # 4
     [40.21, 82.41, 0],  # 5
     [40.68, 82.29, 0],  # 6
     [40.74, 81.70, 0]])  # 7

if __name__ == "__main__":
    # np.save('../../tests/matrix/adjacency_matrix.npy', destination_points)
    # np.save('../../tests/matrix/adjacency_matrix.npy', map_destination)
    np.savez('../../tools/draw_graph/adjacency_matrix.npz',
             destination_points=destination_points,
             map_destination=map_destination)
