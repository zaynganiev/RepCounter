import cv2
import numpy as np
from sklearn.svm import LinearSVC

# Keep the image shape consistent so reshape does not fail.
TARGET_SIZE = (150, 150)
TARGET_LEN = TARGET_SIZE[0] * TARGET_SIZE[1]


class Model:

    def __init__(self):
        self.model = LinearSVC()
        self.trained = False

    def _load_and_flatten(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        resized = cv2.resize(img, TARGET_SIZE)
        return resized.reshape(TARGET_LEN)

    def train_model(self, counters):
        img_list = []
        class_list = []

        for i in range(1, counters[0]):
            img = self._load_and_flatten(f"1/frame{i}.jpg")
            if img is not None:
                img_list.append(img)
                class_list.append(1)

        for i in range(1, counters[1]):
            img = self._load_and_flatten(f"2/frame{i}.jpg")
            if img is not None:
                img_list.append(img)
                class_list.append(2)

        if not img_list:
            print("No training images found.")
            return False

        img_array = np.vstack(img_list)
        class_array = np.array(class_list)
        if np.unique(class_array).shape[0] < 2:
            print("Need samples for both classes before training.")
            return False

        self.model.fit(img_array, class_array)
        self.trained = True
        print("Model trained successfully.")
        return True

    def predict(self, frame):
        if not self.trained:
            print("Model not trained yet.")
            return None

        try:
            frame = frame[1]
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            resized = cv2.resize(gray, TARGET_SIZE)
            flattened = resized.reshape(TARGET_LEN)
            prediction = self.model.predict([flattened])
            return prediction[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
