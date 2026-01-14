import tkinter as tk
import os
import PIL.Image, PIL.ImageTk
import cv2
import camera

class App:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rep Counter")

        self.counters = [1, 1]
        self.rep_counter = 0

        self.extended = False
        self.contracted = False
        self.last_prediction = 0

        self.model = None  # Placeholder for the model class

        self.counting_enabled = False

        self.camera = camera.Camera()

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes("-topmost", True)
        self.window.mainloop()

    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto = tk.Button(self.window, text="Toggle Counting", width=50, command=self.counting_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_one = tk.Button(self.window, text="Extended", width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text="Contracted", width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train(anchor=tk.CENTER, expand=True)

    def update(self):
        pass

    def counting_toggle(self):
        pass

    def save_for_class(self, class_num):
        pass