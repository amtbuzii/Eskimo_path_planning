import tkinter as tk
from tkinter import Menu, Frame
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import constant
import FileHandler.FileHandler as fh
from FieldManager.FieldManager import FieldManager
from GraphCreator.GraphCreator import GraphCreator
import random
import time
from Point.Point import Point
import logging

logging.basicConfig(
    filename="test.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class PointPlotter(Frame):
    def __init__(self, root, field_size, start_point, end_point):
        super().__init__()
        self.root = root
        self.field_size = field_size
        self.start_point = start_point
        self.end_point = end_point
        self.message_label = tk.Label(
            root,
            text="Please select start point",
            fg="light green",
            bg="dark green",
            font="Helvetica 16 bold italic",
        )
        self.message_label.pack()

        self.seed = random.randint(0, 500)

        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.set_xlim((0, field_size))
        self.ax.set_ylim((0, field_size))

        self.canvas = FigureCanvasTkAgg(self.figure, master=root)

        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.pack(side=tk.TOP)
        self.toolbar.update()

        self.canvas.get_tk_widget().pack()
        self.canvas.tkcanvas.pack()

        self.change_seed_button = tk.Button(
            self.toolbar,
            text="Change Seed",
            compound=tk.TOP,
            command=self.change_seed,
            relief=tk.RAISED,
            borderwidth=2,
        )
        self.change_seed_button.pack(side=tk.LEFT, padx=0, pady=0)

        self.reset_button = tk.Button(
            self.toolbar,
            text="Reset",
            compound=tk.RIGHT,
            command=self.reset,
            relief=tk.RAISED,
            borderwidth=2,
        )
        self.reset_button.pack(side=tk.LEFT, padx=0, pady=0)

        self.exit_button = tk.Button(
            self.toolbar,
            text="Exit",
            compound=tk.RIGHT,
            command=self.exit_program,
            relief=tk.RAISED,
            borderwidth=2,
        )
        self.exit_button.pack(side=tk.LEFT, padx=0, pady=0)

        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.option_buttons = []
        options = [
            "Field before convex hull",
            "Field after convex hull",
            "Naive",
            "Greedy",
            "Optimal",
            "RRT",
            "Dubins",
        ]

        for i, option in enumerate(options):
            button = tk.Button(
                root,
                text=option,
                command=lambda index=i: self.run_option(index),
                relief=tk.RAISED,
                borderwidth=2,
            )

            # button.pack(side=tk.LEFT, pady=5)
            button.pack(side=tk.LEFT, anchor=tk.W, pady=5)

            self.option_buttons.append(button)

    def change_seed(self):
        self.seed = random.randint(0, 500)
        print("New seed:", self.seed)

    def reset(self):
        self.start_point = None
        self.end_point = None
        self.message_label.config(text="Please select start point")
        self.ax.clear()
        self.ax.set_xlim((0, self.field_size))
        self.ax.set_ylim((0, self.field_size))
        self.canvas.draw()

        print("Reset")

    def exit_program(self):
        app.root.destroy()

    def on_click(self, event):
        x, y = event.xdata, event.ydata
        if self.start_point is None:
            self.start_point = (x, y)
            self.ax.plot(x, y, marker="P", color="red", markersize=10)
            self.message_label.config(text="Please select end point")
        elif self.end_point is None:
            self.end_point = (x, y)
            self.ax.plot(x, y, marker="*", color="red", markersize=10)

        self.canvas.draw()

    def run_option(self, index):
        if self.start_point is not None and self.end_point is not None:
            self.ax.clear()
            main(field_size, self.start_point, self.end_point, index + 1, self.seed)
            self.canvas.draw()

        else:
            print("Please select a start point and an end point.")


def get_field_size():
    field_size = simpledialog.askinteger(
        "Field Size", "Enter the field size (200-400):"
    )
    return field_size if field_size else 5


def main(field_size, start_point, end_point, index, seed):
    # Step 1: Field parameters
    start_point = Point(start_point[0], start_point[1])
    end_point = Point(end_point[0], end_point[1])
    rand_seed = seed

    # Step 2: Start the program - create the field and write to file
    field_m = FieldManager(
        size=field_size, start=start_point, end=end_point, seed=rand_seed
    )
    logging.info("Field FieldManager success")
    logging.info("Field seed: {}".format(rand_seed))
    logging.info("Field size: {}".format(field_size))

    test_field = fh.read_field(constant.FILE_PATH)

    if index == 1:
        # Step 3: Read from file and show the field
        fh.show_field(test_field, convex=False)

    elif index == 2:
        # Step 4 - Convex Hull
        test_field.polygons = field_m.get_convexhull_polygons()
        fh.show_field(test_field, convex=True)
        gc = GraphCreator(test_field)
    elif index == 3:
        # Step 5 - Create naive Graph and find the Shortest Path
        test_field.polygons = field_m.get_convexhull_polygons()
        gc = GraphCreator(test_field)

        start_time = time.time()
        gc.create_graph(graph_type="Naive")
        naive_length = gc.shortest_path()
        naive_runtime = time.time() - start_time
        logging.info("naive length: {}".format(naive_length))
        logging.info("naive time: {}".format(naive_runtime))
        gc.draw_graph()
    elif index == 5:
        # Step 6 - Create optimal Graph and find the Shortest Path
        test_field.polygons = field_m.get_convexhull_polygons()
        gc = GraphCreator(test_field)

        start_time = time.time()
        gc.create_graph(graph_type="Optimal")
        optimal_length = gc.shortest_path()
        optimal_runtime = time.time() - start_time
        logging.info("optimal length: {}".format(optimal_length))
        logging.info("optimal time: {}".format(optimal_runtime))
        gc.draw_graph()
    elif index == 4:
        # Step 7 - Create optimal* Graph and find the Shortest Path
        test_field.polygons = field_m.get_convexhull_polygons()
        gc = GraphCreator(test_field)

        start_time = time.time()
        gc.create_graph(graph_type="Greedy")
        greedy_length = gc.shortest_path()
        greedy_runtime = time.time() - start_time
        logging.info("greedy length: {}".format(greedy_length))
        logging.info("greedy time: {}".format(greedy_runtime))
        gc.draw_graph()
    elif index == 6:
        # Step 8 - Create RRT Graph and find the Shortest Path
        test_field.polygons = field_m.get_convexhull_polygons()
        gc = GraphCreator(test_field)

        start_time = time.time()
        gc.create_graph(graph_type="RRT")
        random_length = gc.shortest_path()
        random_runtime = time.time() - start_time
        logging.info("RRT length: {}".format(random_length))
        logging.info("RRT time: {}".format(random_runtime))
        gc.draw_graph()
    elif index == 7:
        # Step 9 - Dubins extension
        test_field.polygons = field_m.get_convexhull_polygons()
        gc = GraphCreator(test_field)

        start_time = time.time()
        gc.create_graph(graph_type="Dubins")
        dubins_length = gc.get_dubins_path_length()
        dubins_runtime = time.time() - start_time
        logging.info("Dubins length: {}".format(dubins_length))
        logging.info("Dubins time: {}".format(dubins_runtime))
        gc.draw_graph()
    else:
        return


if __name__ == "__main__":
    root = tk.Tk()
    field_size = get_field_size()
    app = PointPlotter(root, field_size, None, None)
    root.mainloop()
