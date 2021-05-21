import dlib
import cv2
import os
from tkinter import messagebox
import time
from DetectorsClasses.Detector import Detector


class HOGFaceDetection(Detector):
    def __init__(self, image_name, upsampling_number):
        super().__init__(image_name)
        self.__upsampling_number = None
        self.set_upsampling_number(upsampling_number)
        self.set_image_path(image_name)

    def detect_face(self):
        end = start = 0
        if self._are_all_variables_set():
            self._img = dlib.load_rgb_image(self._image_name)
            self.__hog_face_detector = dlib.get_frontal_face_detector()
            start = time.time()
            faces = self.__hog_face_detector(self._img, self.__upsampling_number)
            end = time.time()
            for face in faces:
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y

                # draw box over face
                cv2.rectangle(self._img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        else:
            messagebox.showerror("Settings error", "Detection is not available due to settings")
        return self._img, end - start

    def set_image_path(self, path):
        if os.path.exists(str(path)):
            self._image_name = path
        else:
            messagebox.showerror("File error", "Image is not uploaded")

    def get_image_path(self):
        return self._image_name

    def set_upsampling_number(self, pooling_layers):
        if type(pooling_layers) is int:
            if 0 <= pooling_layers <= 4:
                self.__upsampling_number = pooling_layers
            else:
                messagebox.showerror("Value error", "Variable \'upsampling_number\' is out of range")
        else:
            messagebox.showerror("Type error", "Variable \'upsampling_number\' must be int")

    def get_upsampling_number(self):
        return self.__upsampling_number

    def _are_all_variables_set(self):
        return self._image_name and self.__upsampling_number != None
