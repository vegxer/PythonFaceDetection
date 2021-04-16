import dlib
import cv2
import os.path
from tkinter import messagebox
import time


class DlibFaceDetection:
    def __init__(self, image_name, training_file, pooling_layers):
        self.__img = self.__training_file = self.__pooling_layers = self.__image_name = None
        self.set_training_file(training_file)
        self.set_pooling_layers(pooling_layers)
        self.set_image_path(image_name)

    def detect_face(self):
        end = start = 0
        if self.__are_all_variables_set():
            self.__img = dlib.load_rgb_image(self.__image_name)
            cnn_face_detector = dlib.cnn_face_detection_model_v1(self.__training_file)
            start = time.time()
            faces = cnn_face_detector(self.__img, self.__pooling_layers)
            end = time.time()
            for face in faces:
                x = face.rect.left()
                y = face.rect.top()
                w = face.rect.right() - x
                h = face.rect.bottom() - y

                # draw box over face
                cv2.rectangle(self.__img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        else:
            messagebox.showerror("Settings error", "Detection is not available due to settings")
        return self.__img, end - start

    def set_image_path(self, path):
        if os.path.exists(str(path)):
            self.__image_name = path
        else:
            messagebox.showerror("File error", "Image is not uploaded")

    def get_image_path(self):
        return self.__image_name

    def set_training_file(self, file):
        if os.path.exists(str(file)):
            self.__training_file = file
        else:
            messagebox.showerror("File error", "Training file is not uploaded")

    def get_training_file(self):
        return self.__training_file

    def set_pooling_layers(self, pooling_layers):
        if type(pooling_layers) is int:
            if 0 <= pooling_layers <= 3:
                self.__pooling_layers = pooling_layers
            else:
                messagebox.showerror("Value error", "Variable \'pooling_layers\' is out of range")
        else:
            messagebox.showerror("Type error", "Variable \'pooling_layers\' must be int")

    def get_pooling_layers(self):
        return self.__pooling_layers

    def __are_all_variables_set(self):
        return self.__image_name and self.__pooling_layers != None and self.__training_file
