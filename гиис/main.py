#
from tkinter import *
from tkinter import ttk

import sys

from loguru import logger

from methods import DDA
from methods import Bresenham
from methods import Wu

from methods.ellipse import ellipse
from methods.parabola import parabola
from methods.hyperbola import hyperbola

from methods.b_spline import b_spline
from methods.bezye import bezye
from methods.ermit import ermit

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add("out.log")

"""
window layout
"""
window = Tk()
window.title("Graphical Editor")
window.geometry("800x700")
window.configure(bg='yellow')

buttons_frame = Frame(window)
buttons_frame.grid(row=1, column=0)
"""
canvas layout
"""
canvas = Canvas(buttons_frame, width=800, height=500, background="white")
canvas.grid(row=0, column=0)

clear_canvas_button = Button(buttons_frame, text="Clear canvas", width=100, background='blue')
clear_canvas_button.grid(row=6, column=0)

"""
Debug
"""
debug_frame = Frame(buttons_frame)
debug_frame.grid(row=4, column=0)

debug_button = Button(debug_frame, text="Debug")
debug_button.grid(row=0, column=1)

"""
figure frame
"""

figure_frame = Frame(buttons_frame)
figure_frame.grid(row=2, column=0)

"""
methods menu layout
"""
line_frame = Frame(figure_frame, highlightbackground="black", highlightthickness=1)
line_frame.grid(row=0, column=0, padx=2, pady=2)

line_label = Label(line_frame, text="Figures", font="Arial")
line_label.grid()

algorithms = ["DDA", "Bresenham", "Wu's line algorithm", "Circle", "Ellipse", "Parabola", "Hyperbola", "B-spline",
              "Ermit", "Bezye"]
line_box = ttk.Combobox(line_frame, values=algorithms, state="readonly", width=100)
line_box.current(0)
line_box.grid()

vector_frame = Frame(window, pady=5)
vector_frame.grid(row=3, column=0)

x_1_label = Label(vector_frame, text="x_1")
x_1_label.grid(row=0, column=0)
x_1_text = Text(vector_frame, height=1, width=4)
x_1_text.grid(row=0, column=1)

y_1_label = Label(vector_frame, text="y_1")
y_1_label.grid(row=0, column=2)
y_1_text = Text(vector_frame, height=1, width=4)
y_1_text.grid(row=0, column=3)

x_2_label = Label(vector_frame, text="x_2")
x_2_label.grid(row=1, column=0)
x_2_text = Text(vector_frame, height=1, width=4)
x_2_text.grid(row=1, column=1)

y_2_label = Label(vector_frame, text="y_2")
y_2_label.grid(row=1, column=2)
y_2_text = Text(vector_frame, height=1, width=4)
y_2_text.grid(row=1, column=3)

"""
events
"""

draw = list()


def choose_figure(event):
    if len(draw) == 2:
        draw.clear()

    logger.debug(f"algorithm: {line_box.get()}")
    logger.debug(event)

    if len(draw) < 2:
        print("x", event)
        draw.append(event)

    if len(draw) == 2:
        s = line_box.get()
        if s in ["DDA", "Bresenham", "Wu's line algorithm"]:
            figure_click(event)
        elif s == "Ellipse":
            draw_ellipse(event)
        elif s == "Circle":
            draw_circle(event)
        elif s == "Parabola":
            draw_parabola(event)
        elif s == "Hyperbola":
            draw_hyperbola(event)
        elif s in ["B-spline", "Ermit", "Bezye"]:
            draw_curva(event)

    print(draw)


def draw_curva(event):
    start_point = (draw[0].x, draw[0].y)
    input_x1_y1 = (int(x_1_text.get("1.0", "end-1c")), int(y_1_text.get("1.0", "end-1c")))
    input_x2_y2 = (int(x_2_text.get("1.0", "end-1c")), int(y_2_text.get("1.0", "end-1c")))
    endpoint = (draw[1].x, draw[1].y)
    print(start_point, input_x1_y1, input_x2_y2, endpoint)
    if line_box.get() == "B-spline":
        points = b_spline(start_point, input_x1_y1, input_x2_y2, endpoint, 1001)
    elif line_box.get() == "Bezye":
        points = bezye(start_point, input_x1_y1, input_x2_y2, endpoint, 1001)
    elif line_box.get() == "Ermit":
        # input_x1_y1 is r0, input_x2_y2 is r1
        points = ermit(p0=start_point, p1=endpoint, r0=input_x1_y1, r1=input_x2_y2, points_amount=1001)

    for i in range(len(points)):
        canvas.create_rectangle(points[i][0], points[i][1], points[i][0] + 1, points[i][1] + 1)


def draw_ellipse(event):
    r_x = abs(draw[0].x - draw[1].x) // 2
    r_y = abs(draw[0].y - draw[1].y) // 2

    x_c = min(draw[0].x, draw[1].x) + r_x
    y_c = min(draw[0].y, draw[1].y) + r_y
    pixels = ellipse(r_x, r_y, x_c, y_c)
    print(pixels)
    for i in range(len(pixels)):
        canvas.create_rectangle(pixels[i][0], pixels[i][1], pixels[i][0] + 1, pixels[i][1] + 1)


def draw_circle(event):
    r_x = abs(draw[0].x - draw[1].x) // 2
    r_y = abs(draw[0].y - draw[1].y) // 2
    r_x = min(r_x, r_y)
    r_y = r_x

    x_c = min(draw[0].x, draw[1].x) + r_x
    y_c = min(draw[0].y, draw[1].y) + r_y
    pixels = ellipse(r_x, r_y, x_c, y_c)
    print(pixels)
    for i in range(len(pixels)):
        canvas.create_rectangle(pixels[i][0], pixels[i][1], pixels[i][0] + 1, pixels[i][1] + 1)


def draw_parabola(event):
    x1, y1 = draw[0].x, draw[0].y
    x2, y2 = draw[1].x, draw[1].y
    pixels = parabola(x1, y1, x2, y2)
    print(pixels)
    for i in range(len(pixels)):
        canvas.create_rectangle(pixels[i][0], pixels[i][1], pixels[i][0] + 1, pixels[i][1] + 1)


def draw_hyperbola(event):
    x1, y1 = draw[0].x, draw[0].y
    x2, y2 = draw[1].x, draw[1].y
    pixels = hyperbola(x1, y1, x2, y2)
    print(pixels)
    for i in range(len(pixels)):
        canvas.create_rectangle(pixels[i][0], pixels[i][1], pixels[i][0] + 1, pixels[i][1] + 1)


def figure_click(event):
    """
    Click to draw line.
    """

    points = list()
    if line_box.get() == "DDA":
        points = DDA.DDA(draw[0], draw[1])
    elif line_box.get() == "Bresenham":
        points = Bresenham.Bresenham(draw[0], draw[1])

    for i in points:
        canvas.create_rectangle(i[0], i[1], i[0] + 1, i[1] + 1, fill="black")

    if line_box.get() == "Wu's line algorithm":
        points, additional, change_flag = Wu.Wu(draw[0], draw[1])
        s1 = 1 if points[-1][0] > points[0][0] else -1
        s2 = 1 if points[-1][1] > points[0][1] else -1

        k = (points[-1][1] - points[0][1]) / (points[-1][0] - points[0][0])
        b = points[-1][1] - points[-1][0] * k
        for i in range(len(points)):
            if change_flag:
                additional[i] = (
                    additional[i][0] - 10 * s1, additional[i][1], abs(points[i][0] * k + b - points[i][1]))
            else:
                additional[i] = (
                    additional[i][0], additional[i][1] - 10 * s2, abs(points[i][0] * k + b - points[i][1]))

        for i in range(len(points)):
            color_1 = "#%02x%02x%02x" % (
                abs(int(255 * additional[i][2])), abs(int(255 * additional[i][2])),
                abs(int(255 * additional[i][2])))

            color_2 = "#%02x%02x%02x" % (
                abs(int(255 * (1 - additional[i][2]))), abs(int(255 * (1 - additional[i][2]))),
                abs(int(255 * (1 - additional[i][2]))))

            print("color ", color_1, len(color_1))
            canvas.create_rectangle(points[i][0], points[i][1], points[i][0] + 1, points[i][1] + 1, fill=color_1)
            canvas.create_rectangle(additional[i][0], additional[i][1], additional[i][0] + 1, additional[i][1] + 1,
                                    fill=color_2)

    logger.debug("line is drown!")


def clear_canvas(event):
    """
    Clear canvas function
    """
    draw.clear()
    logger.debug("now canvas is clear")
    canvas.delete("all")


def choose_debug(event):
    s = line_box.get()

    if s in ["DDA", "Bresenham", "Wu's line algorithm"]:
        debug_line(event)
    elif s == "Ellipse":
        debug_ellipse(event)
    elif s == "Circle":
        debug_circle(event)
    elif s == "Parabola":
        debug_parabola(event)
    elif s == "Hyperbola":
        debug_hyperbola(event)
    elif s == "B-spline":
        debug_curva(event, "B-spline")
    elif s == "Bezye":
        debug_curva(event, "Bezye")
    elif s == "Ermit":
        debug_curva(event, "Ermit")


def debug_ellipse(event):
    if len(draw) != 2:
        return

    debug_window = Tk()
    debug_window.title("Debug")
    debug_window.geometry("600x600")

    next_button = Button(debug_window, text="Next")
    next_button.grid()

    debug_canvas = Canvas(debug_window, width=500, height=500, background="white")
    debug_canvas.grid()

    r_x = abs(draw[0].x - draw[1].x) // 2
    r_y = abs(draw[0].y - draw[1].y) // 2

    x_c = min(draw[0].x, draw[1].x) + r_x
    y_c = min(draw[0].y, draw[1].y) + r_y
    points = ellipse(r_x, r_y, x_c, y_c)

    def debug_draw(event):
        debug_canvas.create_rectangle(points[0][0], points[0][1], points[0][0] + 1, points[0][1] + 1,
                                      fill="black")
        points.pop(0)

    next_button.bind("<Button-1>", debug_draw)


def debug_circle(event):
    if len(draw) != 2:
        return

    debug_window = Tk()
    debug_window.title("Debug")
    debug_window.geometry("600x600")

    next_button = Button(debug_window, text="Next")
    next_button.grid()

    debug_canvas = Canvas(debug_window, width=500, height=500, background="white")
    debug_canvas.grid()

    r_x = abs(draw[0].x - draw[1].x) // 2
    r_y = abs(draw[0].y - draw[1].y) // 2
    r_x = min(r_x, r_y)
    r_y = r_x

    x_c = min(draw[0].x, draw[1].x) + r_x
    y_c = min(draw[0].y, draw[1].y) + r_y
    points = ellipse(r_x, r_y, x_c, y_c)

    def debug_draw(event):
        debug_canvas.create_rectangle(points[0][0], points[0][1], points[0][0] + 1, points[0][1] + 1,
                                      fill="black")
        points.pop(0)

    next_button.bind("<Button-1>", debug_draw)


def debug_parabola(event):
    if len(draw) != 2:
        return

    debug_window = Tk()
    debug_window.title("Debug")
    debug_window.geometry("600x600")

    next_button = Button(debug_window, text="Next")
    next_button.grid()

    debug_canvas = Canvas(debug_window, width=500, height=500, background="white")
    debug_canvas.grid()

    x1, y1 = draw[0].x, draw[0].y
    x2, y2 = draw[1].x, draw[1].y

    points = parabola(x1, y1, x2, y2)

    def debug_draw(event):
        debug_canvas.create_rectangle(points[0][0], points[0][1], points[0][0] + 1, points[0][1] + 1,
                                      fill="black")
        points.pop(0)

    next_button.bind("<Button-1>", debug_draw)


def debug_hyperbola(event):
    if len(draw) != 2:
        return

    debug_window = Tk()
    debug_window.title("Debug")
    debug_window.geometry("600x600")

    next_button = Button(debug_window, text="Next")
    next_button.grid()

    debug_canvas = Canvas(debug_window, width=500, height=500, background="white")
    debug_canvas.grid()

    x1, y1 = draw[0].x, draw[0].y
    x2, y2 = draw[1].x, draw[1].y

    points = hyperbola(x1, y1, x2, y2)

    def debug_draw(event):
        debug_canvas.create_rectangle(points[0][0], points[0][1], points[0][0] + 1, points[0][1] + 1,
                                      fill="black")
        points.pop(0)

    next_button.bind("<Button-1>", debug_draw)


def debug_line(event):
    debug_window = Tk()
    debug_window.title("Debug")
    debug_window.geometry("600x600")

    next_button = Button(debug_window, text="Next")
    next_button.grid()

    debug_canvas = Canvas(debug_window, width=500, height=500, background="white")
    debug_canvas.grid()

    if line_box.get() == "DDA":
        points = DDA.DDA(draw[0], draw[1])
    elif line_box.get() == "Bresenham":
        points = Bresenham.Bresenham(draw[0], draw[1])

    if line_box.get() == "Wu's line algorithm":
        points, additional, change_flag = Wu.Wu(draw[0], draw[1])
        sign_x = 1
        sign_y = 1
        if additional[-1][0] - additional[0][0] < 0:
            sign_x = -1
        if additional[-1][1] - additional[0][1] < 0:
            sign_y = -1

        prev_x = additional[0][0]
        prev_y = additional[0][1]

        prev_add_x = additional[0][0]
        prev_add_y = additional[0][1]

        pixels = list(additional)
        x = 0
        y = 0
        for i in range(len(additional)):
            if pixels[i][0] == prev_x:
                additional[i] = (prev_add_x, prev_add_y, additional[i][2])
            else:
                additional[i] = (pixels[i][0] + 10 * x * sign_x, prev_add_y, additional[i][2])
                prev_add_x = pixels[i][0] + 10 * x * sign_x
                prev_x = pixels[i][0]
                x += 1

            if pixels[i][1] == prev_y:
                additional[i] = (prev_add_x, prev_add_y, additional[i][2])
            else:
                additional[i] = (prev_add_x, pixels[i][1] + 10 * y * sign_y, additional[i][2])
                prev_add_y = pixels[i][1] + 10 * y * sign_y
                prev_y = pixels[i][1]
                y += 1

    sign_x = 1
    sign_y = 1
    if points[-1][0] - points[0][0] < 0:
        sign_x = -1
    if points[-1][1] - points[0][1] < 0:
        sign_y = -1

    prev_x = points[0][0]
    prev_y = points[0][1]

    prev_add_x = points[0][0]
    prev_add_y = points[0][1]

    pixels = list(points)
    x = 0
    y = 0
    for i in range(len(points)):
        if pixels[i][0] == prev_x:
            points[i] = (prev_add_x, prev_add_y)
        else:
            points[i] = (pixels[i][0] + 10 * x * sign_x, prev_add_y)
            prev_add_x = pixels[i][0] + 10 * x * sign_x
            prev_x = pixels[i][0]
            x += 1

        if pixels[i][1] == prev_y:
            points[i] = (prev_add_x, prev_add_y)
        else:
            points[i] = (prev_add_x, pixels[i][1] + 10 * y * sign_y)
            prev_add_y = pixels[i][1] + 10 * y * sign_y
            prev_y = pixels[i][1]
            y += 1

    def debug_draw(event):
        if line_box.get() == "DDA" or line_box.get() == "Bresenham":
            debug_canvas.create_rectangle(points[0][0], points[0][1], points[0][0] + 10, points[0][1] + 10,
                                          fill="black")
            points.pop(0)
        elif line_box.get() == "Wu's line algorithm":
            color_1 = "#%02x%02x%02x" % (
                abs(int(255 * additional[0][2])), abs(int(255 * additional[0][2])),
                abs(int(255 * additional[0][2])))

            color_2 = "#%02x%02x%02x" % (
                abs(int(255 * (1 - additional[0][2]))), abs(int(255 * (1 - additional[0][2]))),
                abs(int(255 * (1 - additional[0][2]))))

            print("color ", color_1, len(color_1))
            debug_canvas.create_rectangle(points[0][0], points[0][1], points[0][0] + 10, points[0][1] + 10,
                                          fill=color_1)
            debug_canvas.create_rectangle(additional[0][0], additional[0][1], additional[0][0] + 10,
                                          additional[0][1] + 10,
                                          fill=color_2)
            points.pop(0)
            additional.pop(0)

    next_button.bind("<Button-1>", debug_draw)


def debug_curva(event, linebox_value):
    if len(draw) != 2:
        return

    debug_window = Tk()
    debug_window.title("Debug")
    debug_window.geometry("600x600")

    next_button = Button(debug_window, text="Next")
    next_button.grid()

    debug_canvas = Canvas(debug_window, width=500, height=500, background="white")
    debug_canvas.grid()

    p0 = (draw[0].x, draw[0].y)
    p1 = (int(x_1_text.get("1.0", "end-1c")), int(y_1_text.get("1.0", "end-1c")))
    p2 = (int(x_2_text.get("1.0", "end-1c")), int(y_2_text.get("1.0", "end-1c")))
    p3 = (draw[1].x, draw[1].y)
    print(p0, p1, p2, p3)
    if linebox_value == "B-spline":
        points = b_spline(p0, p1, p2, p3, 1000)
    elif linebox_value == "Bezye":
        points = bezye(p0, p1, p2, p3, 1000)
    elif linebox_value == "Ermit":
        points = ermit(p0, p1, p2, p3, 1000)

    def debug_draw(event):
        debug_canvas.create_rectangle(points[0][0], points[0][1], points[0][0] + 1, points[0][1] + 1,
                                      fill="black")
        points.pop(0)

    next_button.bind("<Button-1>", debug_draw)


"""
event bindings
"""
canvas.bind("<Button-1>", choose_figure)
clear_canvas_button.bind("<Button-1>", clear_canvas)

debug_button.bind("<Button-1>", choose_debug)

window.mainloop()