import tkinter as tk
import os
import PIL.Image, PIL.ImageTk
import cv2
import camera
import model

class App:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rep Counter")

        self.counters = [1, 1]
        self.rep_counter = 0

        self.extended = False
        self.contracted = False
        self.last_prediction = 0

        self.model = model.Model()

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

        self.btn_toggleauto = tk.Button(self.window, text="Toggle Counting", width=50, command=self.counting_toggle, state=tk.DISABLED)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_one = tk.Button(self.window, text="Extended", width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text="Contracted", width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=self.train_model)
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.counter_label = tk.Label(self.window, text=f"{self.rep_counter}")
        self.counter_label.config(font=("Arial", 24))
        self.counter_label.pack(anchor=tk.CENTER, expand=True)

        self.status_label = tk.Label(self.window, text="Not trained. Capture samples, then train.")
        self.status_label.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        if self.counting_enabled:
            self.predict()

        if self.extended and self.contracted:
            self.extended, self.contracted = False, False
            self.rep_counter += 1

        self.counter_label.config(text=f"{self.rep_counter}")

        ret, frame = self.camera.get_frame()
        if ret: 
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        if not self.model.trained:
            return

        ret, frame = self.camera.get_frame()
        if ret:
            prediction = self.model.predict((ret, frame))

            if prediction is not None and prediction != self.last_prediction:
                if prediction == 1:
                    self.extended = True
                    self.last_prediction = 1
                if prediction == 2:
                    self.contracted = True
                    self.last_prediction = 2

    def counting_toggle(self):
        if not self.model.trained:
            self.status_label.config(text="Train the model before counting.")
            return
        self.counting_enabled = not self.counting_enabled
        state = "Counting..." if self.counting_enabled else "Paused."
        self.status_label.config(text=state)

    def train_model(self):
        trained = self.model.train_model(self.counters)
        if trained:
            self.btn_toggleauto.config(state=tk.NORMAL)
            self.status_label.config(text="Trained. Click Toggle Counting to start.")
        else:
            self.status_label.config(text="Training failed. Add samples for both classes.")

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not ret:
            return

        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")

        img_path = f"{class_num}/frame{self.counters[class_num-1]}.jpg"
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        resized = cv2.resize(gray, model.TARGET_SIZE)
        cv2.imwrite(img_path, resized)

        self.counters[class_num-1] += 1

    def reset(self):
        self.rep_counter = 0
