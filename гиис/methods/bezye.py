import numpy as np


def bezye(p0, p1, p2, p3, points_amount):
    Mb = np.array(
        [
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ]
    )  # Матрица Безье

    Gbx = np.array(
        [
            p0[0], p1[0], p2[0], p3[0]
        ]
    ).reshape(4, 1)
    Cx = np.matmul(Mb, Gbx)  # В общем виде (T * Mb) * Gbx == T * (Mb * Gbx)

    Gby = np.array(
        [
            p0[1], p1[1], p2[1], p3[1]
        ]
    ).reshape(4, 1)
    Cy = np.matmul(Mb, Gby)  # В общем виде (T * Mb) * Gby == T * (Mb * Gby)

    points = []
    for intermediate_point in range(points_amount):
        t = intermediate_point / (points_amount - 1)
        T = np.array([pow(t, 3), pow(t, 2), t, 1])

        x = np.matmul(T, Cx)[0]  # Матрица 1х1
        y = np.matmul(T, Cy)[0]  # Матрица 1х1

        points.append((x, y))
    return points


if __name__ == "__main__":
    points = bezye((0, 5), (5, 0), (6, 6), (3, 4), 11)
    print(points)
