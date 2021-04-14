import dlib
import cv2
import os.path
from tkinter import messagebox


class DlibFaceDetection:
    def __init__(self, image_name, training_file, pooling_layers):
        self.__img = None
        self.set_training_file(training_file)
        self.set_pooling_layers(pooling_layers)
        self.set_image_path(image_name)

    def detect_face(self):
        if self.__are_all_variables_set():
            self.__img = dlib.load_rgb_image(self.__image_name)
            cnn_face_detector = dlib.cnn_face_detection_model_v1(self.__training_file)
            faces = cnn_face_detector(self.__img, self.__pooling_layers)
            for face in faces:
                x = face.rect.left()
                y = face.rect.top()
                w = face.rect.right() - x
                h = face.rect.bottom() - y

                # draw box over face
                cv2.rectangle(self.__img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        else:
            messagebox.showerror("Settings error", "Not all settings have been set")
        return self.__img

    def set_image_path(self, path):
        if os.path.exists(path):
            self.__image_name = path
        else:
            raise FileNotFoundError

    def get_image_path(self):
        return self.__image_name

    def set_training_file(self, file):
        if os.path.exists(file):
            self.__training_file = file
        else:
            raise FileNotFoundError

    def get_training_file(self):
        return self.__training_file

    def set_pooling_layers(self, pooling_layers):
        if type(pooling_layers) is int:
            if 0 <= pooling_layers <= 3:
                self.__pooling_layers = pooling_layers
            else:
                raise ValueError
        else:
            raise TypeError

    def get_pooling_layers(self):
        return self.__pooling_layers

    def __are_all_variables_set(self):
        return self.__image_name and self.__pooling_layers != None and self.__training_file
