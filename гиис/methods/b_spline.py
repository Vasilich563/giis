def param3(prev_p, current_p, next_p, next_next_p):
    return (-prev_p + 3 * current_p - 3 * next_p + next_next_p) / 6.


def param2(prev_p, current_p, next_p):
    return (prev_p - 2 * current_p + next_p) / 2.


def param1(prev_p, next_p):
    return (-prev_p + next_p) / 2.


def param0(prev_p, current_p, next_p):
    return (prev_p + 4 * current_p + next_p) / 6.


def b_spline(p0, p1, p2, p3, points_amount):
    points = []
    main_points = (p0, p0, p1, p2, p3, p3, p3)  # расширение p-1 = p0, p3 + 1 = p3, p3 + 2 = p3
    for i in range(1, 4):
        for intermediate_point in range(points_amount):
            t = intermediate_point / (points_amount - 1)
    
            a3 = param3(main_points[i - 1][0], main_points[i][0], main_points[i + 1][0], main_points[i + 2][0])  # x
            a2 = param2(main_points[i - 1][0], main_points[i][0], main_points[i + 1][0])  # x
            a1 = param1(main_points[i - 1][0], main_points[i + 1][0])  # x
            a0 = param0(main_points[i - 1][0], main_points[i][0], main_points[i + 1][0])  # x
            
            b3 = param3(main_points[i - 1][1], main_points[i][1], main_points[i + 1][1], main_points[i + 2][1])  # y
            b2 = param2(main_points[i - 1][1], main_points[i][1], main_points[i + 1][1])  # y
            b1 = param1(main_points[i - 1][1], main_points[i + 1][1])  # y
            b0 = param0(main_points[i - 1][1], main_points[i][1], main_points[i + 1][1])  # y
    
            x_t = ((a3 * t + a2) * t + a1) * t + a0
            y_t = ((b3 * t + b2) * t + b1) * t + b0
    
            points.append((x_t, y_t))
    return points
