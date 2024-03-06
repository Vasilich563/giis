def parabola(x1, y1, x2, y2):

    a = (y2 - y1) / pow((x2 - x1), 2)
    b = -2 * a * x1
    c = y1 - a * pow(x1, 2) - b * x1

    x = min(x1, x2)
    x_max = max(x1, x2)
    y_values = []
    x_values = []

    while x <= x_max:
        y = a * pow(x, 2) + b * x + c
        y_values.append(y)
        x_values.append(x)
        x += 1

    pixels = []

    if x1 < x2:
        for i in range(len(x_values)):
            pixels.append((x_values[i], y_values[i]))
            pixels.append((x_values[i] - 2 * (x_values[i] - x_values[0]), y_values[i]))
    else:
        for i in range(len(x_values)):
            pixels.append((x_values[i], y_values[i]))
            pixels.append((x_values[i] + 2 * (x_values[len(x_values) - 1] - x_values[i]), y_values[i]))
    return pixels