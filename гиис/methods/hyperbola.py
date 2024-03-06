def hyperbola(x1, y1, x2, y2):
    a = abs(x2 - x1) // 2
    b = abs(y2 - y1) // 2
    h = (x1 + x2) // 2
    k = (y1 + y2) // 2
    x = 0
    y = b
    d = pow(b, 2) - pow(a, 2) * b + pow(a, 2) / 4

    pixels = []
    while pow(a, 2) * (2 * y - 1) > 2 * pow(b, 2) * (x + 1):  # Region 1
        if d < 0:  # midpoint is inside hyberbola bound - next is (x + 1, y)
            d = d + pow(b, 2) * (2 * x + 3)
            x = x + 1
        else:  # midpoint is outside hyberbola bound or on it - next is (x + 1, y - 1)
            d = d + pow(b, 2) * (2 * x + 3) + pow(a, 2) * (-2 * y + 2)
            x = x + 1
            y = y - 1
        pixels.append((x + h, -y + k))
        pixels.append((-x + abs(x1 - x2) + h, y - abs(y1 - y2) + k))

    d = pow(b, 2) * pow((x + 1), 2) + pow(a, 2) * pow((y - 1), 2) - pow(a, 2) * pow(b, 2)

    while y > 0:  # Region 2
        if d < 0:  # midpoint is inside hyperbola bound - next is (x + 1, y - 1)
            d = d + pow(b, 2) * (2 * x + 2) + pow(a, 2) * (-2 * y + 3)
            x = x + 1
            y = y - 1
        else:  # midpoint is outside hyperbola bound or on it - next is (x, y - 1)
            d = d + pow(a, 2) * (-2 * y + 3)
            y = y - 1
        pixels.append((x + h, -y + k))
        pixels.append((-x + abs(x1 - x2) + h, y - abs(y1 - y2) + k))

    return pixels