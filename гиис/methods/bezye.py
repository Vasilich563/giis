import numpy as np


def bezier(event_1, event_2, p0, p1, num_samples=1000):
    points = [(event_1.x, event_1.y), p0, p1, (event_2.x, event_2.y)]

    t_values = np.linspace(0, 1, num_samples)
    n = len(points) - 1
    curve_points = []

    for t in t_values:
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt

        x = mt3 * points[0][0] + 3 * mt2 * t * points[1][0] + 3 * mt * t2 * points[2][0] + t3 * points[3][0]
        y = mt3 * points[0][1] + 3 * mt2 * t * points[1][1] + 3 * mt * t2 * points[2][1] + t3 * points[3][1]

        curve_points.append([x, y])

    return curve_points
