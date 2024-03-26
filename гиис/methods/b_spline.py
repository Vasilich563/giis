import numpy as np


def b_spline(p0, p1, p2, p3, points_amount):
    main_points = (p0, p0, p1, p2, p3, p3)  # расширение p-1 = p0, p3 + 1 = p3, p3 + 2 = p3
    Ms = np.array(
        [
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 0, 3, 0],
            [1, 4, 1, 0]
        ]
    ) / 6.  # Коэффициенты в методе б-сплайн

    points = []
    for i in range(1, 4):  # 1 <= i <= n - 1
        Gsx = np.array(
            [
                main_points[i - 1][0], main_points[i][0], main_points[i + 1][0], main_points[i + 2][0]
            ]
        ).reshape(4, 1)  # Точки текущего сегмента по оси x
        Cx = np.matmul(Ms, Gsx)  # В общем виде (T * Ms) * Gsx == T * (Ms * Gsx)

        Gsy = np.array(
            [
                main_points[i - 1][1], main_points[i][1], main_points[i + 1][1], main_points[i + 2][1]
            ]
        ).reshape(4, 1)  # Точки текущего сегмента по оси y
        Cy = np.matmul(Ms, Gsy)  # В общем виде (T * Ms) * Gsy == T * (Ms * Gsy)

        for intermediate_point in range(points_amount):
            t = intermediate_point / (points_amount - 1)
            T = np.array([pow(t, 3), pow(t, 2), t, 1])
    
            x = np.matmul(T, Cx)[0]  # Матрица 1х1
            y = np.matmul(T, Cy)[0]  # Матрица 1х1
    
            points.append((x, y))
    return points
