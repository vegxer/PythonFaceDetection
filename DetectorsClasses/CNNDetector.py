import dlib
import cv2
import os
from tkinter import messagebox
import time
from DetectorsClasses.Detector import Detector


# класс для обнаружения лиц методом CNN
class CNNFaceDetection(Detector):
    def __init__(self, image_name, training_file, pooling_layers):
        super().__init__(image_name)
        self.__training_file = self.__pooling_layers = None
        # установка входных параметров через сеттеры
        self.set_training_file(training_file)
        self.set_pooling_layers(pooling_layers)
        super().set_image_path(image_name)

    # обнаруживает лица на изображении
    def detect_face(self):
        img = None
        end = start = 0
        if self._are_all_variables_set():
            # загрузка изображения
            img = dlib.load_rgb_image(self._image_name)
            self.__cnn_face_detector = dlib.cnn_face_detection_model_v1(self.__training_file)
            # замер времени выполнения алгоритма
            start = time.time()
            faces = self.__cnn_face_detector(img, self.__pooling_layers)
            end = time.time()
            for face in faces:
                # координаты прямоугольников, их ширина и высота
                x = face.rect.left()
                y = face.rect.top()
                w = face.rect.right() - x
                h = face.rect.bottom() - y

                # рисует прямоугольники вокруг лиц
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        else:
            messagebox.showerror("Settings error", "Detection is not available due to settings")
        return img, end - start

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

    def _are_all_variables_set(self):
        return self._image_name and self.__pooling_layers != None and self.__training_file
