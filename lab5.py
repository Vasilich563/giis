import tkinter as tk
from math import atan2


def jarvis_march(points):
    if len(points) < 3:
        return points

    # Находим самую левую точку
    leftmost = min(points, key=lambda p: p[0])

    hull = [leftmost]
    current = leftmost
    next_point = None

    while True:
        next_point = None
        for p in points:
            if p == current:
                continue
            if next_point is None or ccw(current, p, next_point) > 0 or (ccw(current, p, next_point) == 0 and (
                    (p[0] - current[0]) * (next_point[1] - current[1]) - (p[1] - current[1]) * (
                    next_point[0] - current[0])) < 0):
                next_point = p
        if next_point == hull[0]:
            break
        hull.append(next_point)
        current = next_point

    return hull


def graham_scan(points):
    if len(points) < 3:
        return points

    # Находим самую левую точку
    p0 = min(points, key=lambda p: (p[0], p[1]))

    # Сортируем точки в порядке возрастания угла относительно p0
    points.sort(key=lambda p: (atan2(p[1] - p0[1], p[0] - p0[0]), -(p[1] - p0[1]), -(p[0] - p0[0])))

    stack = [p0, points[1]]
    for i in range(2, len(points)):
        while len(stack) > 1 and ccw(stack[-2], stack[-1], points[i]) <= 0:
            stack.pop()
        stack.append(points[i])

    return stack


def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def is_convex(points):
    if len(points) < 3:
        return True
    sign = None
    for i in range(len(points)):
        j = (i + 1) % len(points)
        k = (i + 2) % len(points)
        c = ccw(points[i], points[j], points[k])
        if sign is None:
            sign = 1 if c > 0 else -1 if c < 0 else 0
        elif sign != 1 if c > 0 else -1 if c < 0 else 0:
            return False
    return True


def find_convex_hull(self):
    if len(self.points) < 3 or is_convex(self.points):
        return self.points

    # Удаляем существующие линии с холста
    for line in self.lines:
        self.canvas.delete(line)
    self.lines = []

    algorithm = self.algorithm_var.get()
    if algorithm == "Jarvis":
        hull = jarvis_march(self.points)
    else:
        hull = graham_scan(self.points)

    self.canvas.delete("hull")
    for i in range(len(hull)):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % len(hull)]
        self.canvas.create_line(x1, y1, x2, y2, tags="hull", width=2)

    return hull


def intersection_point(a1, a2, b1, b2):
    """
    Вычисляет точку пересечения двух отрезков.
    a1, a2 - координаты точек начала и конца первого отрезка.
    b1, b2 - координаты точек начала и конца второго отрезка.
    Возвращает координаты точки пересечения или None, если отрезки не пересекаются.
    """
    x1, y1 = a1
    x2, y2 = a2
    x3, y3 = b1
    x4, y4 = b2

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    else:
        return None


class PolygonBuilder(tk.Tk):

    def find_intersection_points(self):
        if len(self.points) < 3:
            return

        self.canvas.delete("intersection")

        segment_x1 = self.segment_x1_entry.get()
        segment_y1 = self.segment_y1_entry.get()
        segment_x2 = self.segment_x2_entry.get()
        segment_y2 = self.segment_y2_entry.get()

        try:
            segment_x1, segment_y1, segment_x2, segment_y2 = float(segment_x1), float(segment_y1), float(
                segment_x2), float(segment_y2)
        except ValueError:
            self.canvas.create_text(400, 550, text="Please enter valid coordinates for the segment.",
                                    tags="intersection")
            return

        segment = ((segment_x1, segment_y1), (segment_x2, segment_y2))

        intersection_points = []
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            intersection = intersection_point(p1, p2, segment[0], segment[1])
            if not intersection is None:
                intersection = (int(intersection[0] * 100) / 100, int(intersection[1] * 100) / 100)
            if intersection:
                intersection_points.append(intersection)

        for x, y in intersection_points:
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", tags="intersection")

        if intersection_points:
            self.canvas.create_text(100, 20, text=f"Точки \n пересечения: {intersection_points}", tags="intersection")
        else:
            self.canvas.create_text(100, 20, text="Полигон не пересекается", tags="intersection")

    def __init__(self):
        super().__init__()
        self.title("Polygon Builder")

        self.canvas = tk.Canvas(self, width=500, height=420, bg="lightblue")
        self.canvas.grid(row=0, column=0, rowspan=4, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Double-1>", self.close_polygon)
        self.points = []
        self.lines = []

        self.segment_frame = tk.Frame(self)
        self.segment_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.segment_x1_label = tk.Label(self.segment_frame, text="Line Poin X1:")
        self.segment_x1_label.grid(row=0, column=0, padx=5, pady=5)
        self.segment_x1_entry = tk.Entry(self.segment_frame)
        self.segment_x1_entry.grid(row=0, column=1, padx=5, pady=5)

        self.segment_y1_label = tk.Label(self.segment_frame, text="Line Poin Y1:")
        self.segment_y1_label.grid(row=1, column=0, padx=5, pady=5)
        self.segment_y1_entry = tk.Entry(self.segment_frame)
        self.segment_y1_entry.grid(row=1, column=1, padx=5, pady=5)

        self.segment_x2_label = tk.Label(self.segment_frame, text="Line Poin X2:")
        self.segment_x2_label.grid(row=2, column=0, padx=5, pady=5)
        self.segment_x2_entry = tk.Entry(self.segment_frame)
        self.segment_x2_entry.grid(row=2, column=1, padx=5, pady=5)

        self.segment_y2_label = tk.Label(self.segment_frame, text="Line Poin Y2:")
        self.segment_y2_label.grid(row=3, column=0, padx=5, pady=5)
        self.segment_y2_entry = tk.Entry(self.segment_frame)
        self.segment_y2_entry.grid(row=3, column=1, padx=5, pady=5)

        self.find_intersection_button = tk.Button(self.segment_frame, text="Find Intersection",
                                                  command=self.find_intersection_points)
        self.find_intersection_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.run_button = tk.Button(self.button_frame, text="Run", command=self.find_convex_hull)
        self.run_button.grid(row=0, column=0, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Jarvis")

        self.algorithm_menu = tk.OptionMenu(self.button_frame, self.algorithm_var, "Jarvis", "Graham")
        self.algorithm_menu.grid(row=0, column=2, padx=5)

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))

        # Создаем новую линию, соединяющую последнюю добавленную точку с предыдущей
        if len(self.points) > 1:
            line = self.canvas.create_line(self.points[-2][0], self.points[-2][1], x, y, width=2)
            self.lines.append(line)

        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="pink")

    def close_polygon(self, event):
        if len(self.points) >= 3:
            # Соединяем последнюю точку с первой
            x1, y1 = self.points[-1]
            x2, y2 = self.points[0]
            line = self.canvas.create_line(x1, y1, x2, y2, width=2)
            self.lines.append(line)

            # Проверяем, является ли полигон выпуклым
            if is_convex(self.points):
                self.canvas.delete("message")
                self.canvas.create_text(400, 50, text="Polygon is convex", tags="message")
                self.find_convex_hull()
            else:
                self.canvas.delete("message")
                self.canvas.create_text(400, 50, text="Polygon is not convex", tags="message")

    def find_convex_hull(self):
        if len(self.points) < 3 or is_convex(self.points):
            return

        # Удаляем существующие линии с холста
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []

        algorithm = self.algorithm_var.get()
        if algorithm == "Jarvis":
            hull = jarvis_march(self.points)
        else:
            hull = graham_scan(self.points)

        self.canvas.delete("hull")
        for i in range(len(hull)):
            x1, y1 = hull[i]
            x2, y2 = hull[(i + 1) % len(hull)]
            self.canvas.create_line(x1, y1, x2, y2, tags="hull", width=2)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.lines = []


if __name__ == "__main__":
    app = PolygonBuilder()
    app.geometry("760x450")
    app.mainloop()
