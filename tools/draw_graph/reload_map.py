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

destination_points = np.array(
    [[34.67, 45.23, 0],  # 0
     [25.67, 67.23, 0],  # 1
     [67.67, 81.23, 1],  # 2
     [12.67, 24.23, 0],  # 3
     [53.67, 31.23, 0],  # 4
     [79.67, 65.23, 0],  # 5
     [15.67, 31.23, 0],  # 6
     [27.67, 57.23, 1]])  # 7

if __name__ == "__main__":
    # np.save('../../tests/matrix/adjacency_matrix.npy', destination_points)
    # np.save('../../tests/matrix/adjacency_matrix.npy', map_destination)
    np.savez('../../tools/draw_graph/adjacency_matrix.npz',
             destination_points=destination_points,
             map_destination=map_destination)
