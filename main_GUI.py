import importlib
import tkinter
import tkinter.messagebox
import customtkinter
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
from PIL import Image
import os
from constant import *


logging.basicConfig(
    filename="test.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.seed = random.randint(0, 600)
        self.field_size = constant.FIELD_SIZE
        self.start_point = None
        self.end_point = None

        # configure window
        self.title("Eskimo - Amit Bouzaglo")
        self.geometry(f"{1100}x{630}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "eskimo.png")), size=(26, 26)
        )
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text=" Eskimo",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.start_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "rocket.png")), size=(26, 26)
        )
        self.reset_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "reset.png")), size=(26, 26)
        )
        self.seed_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "seed.png")), size=(26, 26)
        )
        self.info_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "information.png")), size=(26, 26)
        )
        self.log_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "log-file.png")), size=(26, 26)
        )

        self.sidebar_button_0 = customtkinter.CTkButton(
            self.sidebar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Start",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.start_image,
            anchor="w",
            command=self.start,
        )
        self.sidebar_button_0.grid(row=1, column=0, sticky="ew")

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Reset",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.reset_image,
            anchor="w",
            command=self.reset,
        )
        self.sidebar_button_1.grid(row=2, column=0, sticky="ew")

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Change Seed",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.seed_image,
            anchor="w",
            command=self.change_seed,
        )
        self.sidebar_button_2.grid(row=3, column=0, sticky="ew")

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Log File",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.log_image,
            anchor="w",
            command=self.read_log,
        )
        self.sidebar_button_3.grid(row=4, column=0, sticky="ew")

        self.sidebar_button_4 = customtkinter.CTkButton(
            self.sidebar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="About",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.info_image,
            anchor="w",
            command=self.about,
        )
        self.sidebar_button_4.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI configuration:", anchor="w"
        )
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create start_up screen

        self.center_frame = customtkinter.CTkFrame(self)
        self.center_frame.grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.center_frame.grid_columnconfigure(1, weight=1)
        self.center_frame.grid_rowconfigure(5, weight=1)
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "eskimo.png")), size=(50, 50)
        )

        self._image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "iceberg.png")), size=(400, 300)
        )
        self.open_title = customtkinter.CTkLabel(
            self.center_frame,
            text=" Eskimo",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=50, weight="bold"),
        )
        self.open_title.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.home_frame_large_image_label = customtkinter.CTkLabel(
            self.center_frame, text="", image=self._image
        )
        self.home_frame_large_image_label.grid(
            row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        self.open_title = customtkinter.CTkLabel(
            self.center_frame,
            text="Find the best path from A to B \n avoiding obstacles in a 2D environment.",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.open_title.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.start_bttn = customtkinter.CTkButton(
            self.center_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Start",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.start_image,
            command=self.start,
        )
        self.start_bttn.grid(row=3, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.git_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "pngegg.png")), size=(30, 30)
        )
        self.git_bttn = customtkinter.CTkButton(
            self.center_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Git",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.git_image,
            command=self.open_link,
        )
        self.git_bttn.grid(row=4, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Algorithms")
        self.tabview.add("Constants")
        self.tabview.tab("Algorithms").grid_columnconfigure(
            0, weight=1
        )  # configure grid of individual tabs
        self.tabview.tab("Constants").grid_columnconfigure(0, weight=1)

        # create algorithms

        self.label_tab_2 = customtkinter.CTkLabel(
            self.tabview.tab("Algorithms"), text="Choose Algorithm:"
        )
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.alg_button_1 = customtkinter.CTkButton(
            self.tabview.tab("Algorithms"),
            text="Generate field",
            command=lambda: self.run_option(1),
        )
        self.alg_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.alg_button_2 = customtkinter.CTkButton(
            self.tabview.tab("Algorithms"),
            text="ConvexHull",
            command=lambda: self.run_option(2),
        )
        self.alg_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.alg_button_3 = customtkinter.CTkButton(
            self.tabview.tab("Algorithms"),
            text="Naive",
            command=lambda: self.run_option(3),
        )
        self.alg_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.alg_button_4 = customtkinter.CTkButton(
            self.tabview.tab("Algorithms"),
            text="Greedy",
            command=lambda: self.run_option(4),
        )
        self.alg_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.alg_button_5 = customtkinter.CTkButton(
            self.tabview.tab("Algorithms"),
            text="Optimal",
            command=lambda: self.run_option(5),
        )
        self.alg_button_5.grid(row=5, column=0, padx=20, pady=10)

        self.alg_button_6 = customtkinter.CTkButton(
            self.tabview.tab("Algorithms"),
            text="RRT",
            command=lambda: self.run_option(6),
        )
        self.alg_button_6.grid(row=6, column=0, padx=20, pady=10)

        self.alg_button_7 = customtkinter.CTkButton(
            self.tabview.tab("Algorithms"),
            text="Dubins",
            command=lambda: self.run_option(7),
        )
        self.alg_button_7.grid(row=7, column=0, padx=20, pady=10)

        # change constant
        self.update_const_buttons()

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def about(self) -> None:
        version = "2.0"
        name = "Amit Bouzaglo"
        email = "amitbou@rafael.co.il"

        dialog = customtkinter.CTkToplevel()
        dialog.geometry(f"{400}x{350}")
        dialog.title("About Eskimo")

        # Create and pack labels with the information
        customtkinter.CTkLabel(dialog, text="Version: " + version).pack()
        customtkinter.CTkLabel(dialog, text="Name: " + name).pack()
        customtkinter.CTkLabel(dialog, text="Email: " + email).pack()
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "eskimo.png")), size=(200, 200)
        )
        customtkinter.CTkLabel(dialog, text="j", image=logo_image).pack()
        git_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "pngegg.png")), size=(30, 30)
        )

        self.sidebar_button_0 = customtkinter.CTkButton(
            dialog,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Git",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=git_image,
            command=self.open_link,
        ).pack()

    def read_log(self) -> None:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.log")

        # Read the contents of the log file
        with open(path, "r") as file:
            log_content = file.read()

        dialog = customtkinter.CTkToplevel()
        dialog.geometry(f"{650}x{650}")
        dialog.title("Log file - Eskimo")

        textbox = customtkinter.CTkTextbox(dialog, width=600, height=600)
        textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Create and pack labels with the information

        textbox.insert("0.0", log_content)

    def open_link(self):
        git_link = "https://github.com/amtbuzii/Eskimo_path_planning/"
        git_link = git_link
        import webbrowser

        webbrowser.open(git_link)

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str) -> None:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def on_click(self, event) -> None:
        x, y = event.xdata, event.ydata
        if self.start_point is None:
            self.start_point = (x, y)
            self.ax.plot(x, y, marker="P", color="red", markersize=10)
            self.change_info(text="Please select end point")

        elif self.end_point is None:
            self.end_point = (x, y)
            self.ax.plot(x, y, marker="*", color="red", markersize=10)
            self.change_info(text="Please select algorithm")

        self.canvas.draw()

    def change_seed(self) -> None:
        self.seed = random.randint(0, 600)
        self.change_info(text="New seed: " + str(self.seed))

    def reset(self) -> None:
        self.start_point = None
        self.end_point = None
        # self.change_info(text="Please select start point")
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        self.ax.clear()
        self.field_size = constant.FIELD_SIZE

        self.ax.set_xlim((0, self.field_size))
        self.ax.set_ylim((0, self.field_size))
        self.canvas.draw()

    def start(self) -> None:
        self.canvas_root = customtkinter.CTkCanvas(self, width=250)
        self.canvas_root.grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        self.entry = customtkinter.CTkLabel(self, text="Please select start point")
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.set_xlim((0, self.field_size))
        self.ax.set_ylim((0, self.field_size))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_root)
        self.reset()

        toolbar = NavigationToolbar2Tk(self.canvas, self.canvas_root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.draw()

    def run_option(self, index: int) -> None:
        if self.start_point is not None and self.end_point is not None:
            self.ax.clear()
            text = algorithms(
                self.field_size, self.start_point, self.end_point, index, self.seed
            )
            self.canvas.draw()
            if index not in [1, 2]:
                if text[0] == None:
                    text = "Sorry, No path found, try another algorithm."
                else:
                    text = "Length = {:.3f}, Runtime = {:.3f}".format(text[0], text[1])
                self.change_info(text)

        else:
            self.change_info("Please select a start point and an end point.")

    def change_info(self, text) -> None:
        self.entry = customtkinter.CTkLabel(self, text=text)
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

    def update_const_buttons(self):
        constants_value = [
            (name, value) for name, value in globals().items() if name.isupper()
        ][5:]
        for i, cnst in enumerate(constants_value):
            constant_name = cnst[0]
            try:
                # Import the module containing the constants
                constant_module = importlib.import_module("constant")

                # Get the current value of the constant
                current_value = getattr(constant_module, constant_name)

            except ImportError:
                self.change_info("Failed to import the constant module.")
            except AttributeError:
                self.change_info(f"The constant '{constant_name}' does not exist.")

            label_tab = customtkinter.CTkLabel(
                self.tabview.tab("Constants"),
                text=constant_name + " = " + str(current_value),
                width=2,
            )
            label_tab.grid(row=i, column=0, padx=1, pady=3)

            string_input_button = customtkinter.CTkButton(
                self.tabview.tab("Constants"),
                text="change",
                width=2,
                command=lambda index=constant_name: self.change_const(index),
            )
            string_input_button.grid(row=i, column=1, padx=1, pady=3)

    def change_const(self, constant_name) -> None:
        # Update the value in the globals() dictionary
        dialog = customtkinter.CTkInputDialog(
            text="Type new value for " + constant_name + " (integer only)",
            title="Change Constants",
        )
        new_value = int(dialog.get_input())

        try:
            # Import the module containing the constants
            constant_module = importlib.import_module("constant")

            # Get the current value of the constant
            current_value = getattr(constant_module, constant_name)

            # Update the constant with the new value
            setattr(constant_module, constant_name, new_value)

            # a confirmation message
            self.change_info(
                f"The constant '{constant_name}' has been changed from {current_value} to {new_value}."
            )
        except ImportError:
            self.change_info("Failed to import the constant module.")
        except AttributeError:
            self.change_info(f"The constant '{constant_name}' does not exist.")

        self.update_const_buttons()
        self.reset()


def algorithms(field_size, start_point, end_point, index, seed) -> tuple[float, float]:
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
        return naive_length, naive_runtime
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
        return optimal_length, optimal_runtime

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
        return greedy_length, greedy_runtime
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
        return random_length, random_runtime

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
        return dubins_length, dubins_runtime

    else:
        return


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
