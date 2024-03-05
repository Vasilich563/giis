
def add_pixels(pixels, x, y, center_x, center_y):
    pixels.append((x + center_x, y + center_y))  # 1-st quarter
    pixels.append((-x + center_x, y + center_y))  # 2-nd quarter
    pixels.append((-x + center_x, -y + center_y))  # 3-rd quarter
    pixels.append((x + center_x, -y + center_y))  # 4-th quarter

def ellipse(rx, ry, center_x, center_y):

    pixels = []

    # Region 1
    x = 0  # initial x
    y = ry  # initial y
    parameter = pow(ry, 2) + (1 / 4.) * pow(rx, 2) - ry * pow(rx, 2)  # initial parameter of region 1
    while (2 * x * pow(ry, 2)) < (2 * y * pow(rx, 2)):  # while in region1
        add_pixels(pixels, x, y, center_x, center_y)

        if parameter <= 0:
            # means that the middle point is inside the ellipse bound or on it (the most suitable pixel is (x + 1, y))
            # new parameter
            parameter += pow(ry, 2) * (2 * x + 3)
            x += 1
        else:  # means that the middle point is outside the ellipse bound (the most suitable pixel is (x + 1, y - 1))
            parameter += pow(ry, 2) * (2 * x + 3) + pow(rx, 2) * (1 - 2 * y)
            x += 1
            y -= 1

    # Region 2 initial point is the last point of region 1
    # Initial parameter of region 2
    parameter = pow(ry, 2) * pow(x + (1 / 2.), 2) + pow(rx, 2) * pow(y - 1, 2) - pow(rx, 2) * pow(ry, 2)
    while y >= 0:
        add_pixels(pixels, x, y, center_x, center_y)
        # parameter += pow(ry, 2) * (2 * x + 3)
        if parameter <= 0:
            # means that the middle point is inside the ellipse bound or on it
            # so the most suitable pixel is (x + 1, y - 1)
            parameter += 2 * (x + 1) * pow(ry, 2) + (3 - 2 * y) * pow(rx, 2)
            x += 1
            y -= 1
        else:
            # means that the middle point is outside the ellipse bound (the most suitable pixel is (x, y - 1))
            parameter += (3 - 2 * y) * pow(rx, 2)
            y -= 1

    return pixels
