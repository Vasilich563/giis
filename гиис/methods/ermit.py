import numpy as np


def ermit(p0, p1, r0, r1, points_amount):
    # r0 -- направление касательной в начальной точке (dx0, dy0).
    # r1 -- направление касательной в конечной точке (dx1, dy1)
    Mn = np.array(
        [
            [2, -2, 1, 1],
            [-3, 3, -2, -1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ]
    )  # Матрица эрмитовой формы

    Gnx = np.array(
        [
            p0[0], p1[0], r0[0], r1[0]
        ]
    ).reshape((4, 1))  # Вектор Эрмитовой геометрии для x
    Cx = np.matmul(Mn, Gnx)  # В общем виде (T * Mn) * Gnx == T * (Mn * Gnx)

    Gny = np.array(
        [
            p0[1], p1[1], r0[1], r1[1]
        ]
    ).reshape(4, 1)  # Вектор Эрмитовой геометрии для y
    Cy = np.matmul(Mn, Gny)  # В общем виде (T * Mn) * Gny == T * (Mn * Gny)

    points = []
    for intermediate_point in range(points_amount):
        t = intermediate_point / (points_amount - 1)
        T = np.array([pow(t, 3), pow(t, 2), t, 1])

        x = np.matmul(T, Cx)[0]  # Матрица 1х1
        y = np.matmul(T, Cy)[0]  # Матрица 1х1

        points.append((x, y))
    return points


if __name__ == "__main__":
    points = ermit((0, 0), (1, 0), (0, 1), (1, 0), 11)
    print(points)
