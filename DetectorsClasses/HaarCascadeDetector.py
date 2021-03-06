from tkinter import messagebox
import cv2
import os.path
import time
from DetectorsClasses.Detector import Detector


# класс для обнаружения лиц методом каскадов Хаара
class HaarCascadeFaceDetection(Detector):
    def __init__(self, image_name, xml_file, scale_factor, min_neighbors, min_window_width=None, min_window_height=None,
                 max_window_width=None, max_window_height=None):
        super().__init__(image_name)
        self.__xml_file = self.__scale_factor = self.__min_neighbors = None
        super().set_image_path(image_name)
        self.set_training_file(xml_file)
        self.set_scale_factor(scale_factor)
        self.set_min_neighbors(min_neighbors)
        self.__min_window_width = min_window_width
        self.__min_window_height = min_window_height
        self.__max_window_width = max_window_width
        self.__max_window_height = max_window_height
        if max_window_width != None and max_window_height != None:
            self.set_max_size('{}x{}'.format(max_window_width, max_window_height))
        if min_window_width != None and min_window_height != None:
            self.set_min_size('{}x{}'.format(min_window_width, min_window_height))

    def detect_face(self):
        img = None
        start = end = 0
        if self._are_all_variables_set():
            self.__face_cascade = cv2.CascadeClassifier(self.__xml_file)
            # загрузка изображения
            img = cv2.imread(self._image_name)
            # перевод изоражения в цвет cv2.gray
            self.__gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # замер времени выполнения алгоритма
            start = time.time()
            faces = self.__detect_faces()
            end = time.time()
            # рисует прямоугольники вокруг лиц
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        else:
            messagebox.showerror("Settings error", "Detection is not available due to settings")
        return img, end - start

    # в зависимости от введённых параметров метода обнаруживает лица на изображении
    def __detect_faces(self):
        if self.__min_window_width and self.__max_window_width:
            return self.__face_cascade.detectMultiScale(self.__gray, scaleFactor=self.__scale_factor,
                                                       minNeighbors=self.__min_neighbors,
                                                       minSize=(self.__min_window_width, self.__min_window_height),
                                                       maxSize=(self.__max_window_width, self.__max_window_height))
        elif self.__min_window_width:
            return self.__face_cascade.detectMultiScale(self.__gray, scaleFactor=self.__scale_factor,
                                                       minNeighbors=self.__min_neighbors,
                                                       minSize=(self.__min_window_width, self.__min_window_height))
        elif self.__max_window_width:
            return self.__face_cascade.detectMultiScale(self.__gray, scaleFactor=self.__scale_factor,
                                                       minNeighbors=self.__min_neighbors,
                                                       maxSize=(self.__max_window_width, self.__max_window_height))
        else:
            return self.__face_cascade.detectMultiScale(self.__gray, scaleFactor=self.__scale_factor,
                                                       minNeighbors=self.__min_neighbors)

    def set_training_file(self, path):
        if os.path.exists(str(path)):
            self.__xml_file = path
        else:
            messagebox.showerror("File error", "Training file is not uploaded")

    def get_training_file(self):
        return self.__xml_file

    def set_scale_factor(self, scale_factor):
        if type(scale_factor) is float:
            if 0.001 <= scale_factor <= 2:
                self.__scale_factor = scale_factor
            else:
                messagebox.showerror("Value error", "Variable \'scale-factor\' is out of range")
        else:
            messagebox.showerror("Type error", "Variable \'scale-factor\' must be float")

    def get_scale_factor(self):
        return self.__scale_factor

    def set_min_neighbors(self, min_neighbors):
        if type(min_neighbors) is int:
            if 1000 >= min_neighbors > 0:
                self.__min_neighbors = min_neighbors
            else:
                messagebox.showerror("Value error", "Variable \'min_neighbors\' is out of range")
        else:
            messagebox.showerror("Type error", "Variable \'min_neighbors\' must be integer")

    def get_min_neighbors(self):
        return self.__min_neighbors

    def set_min_size(self, size):
        try:
            width = int(size[0:size.find('x')])
            height = int(size[size.find('x') + 1:])
            if width < 1 or height < 1 or (
                    self.__max_window_width != None and self.__max_window_height < height and self.__max_window_width < width):
                messagebox.showerror("Value error", "Variable \'min_size\' is out of range")
            self.__min_window_width = width
            self.__min_window_height = height
        except:
            (messagebox.showerror("Type error", "Size must be in form WIDTHxHEIGHT"))

    def get_min_size(self):
        return self.__min_window_width, self.__min_window_height

    def set_max_size(self, size):
        try:
            width = int(size[0:size.find('x')])
            height = int(size[size.find('x') + 1:])
            if width < 1 or height < 1 or (
                    self.__min_window_width != None and self.__min_window_height > height and self.__min_window_width > width):
                messagebox.showerror("Value error", "Variable \'max_size\' is out of range")
            self.__max_window_width = width
            self.__max_window_height = height
        except:
            (messagebox.showerror("Type error", "Size must be in form WIDTHxHEIGHT"))

    def get_max_size(self):
        return self.__max_window_width, self.__max_window_height

    def _are_all_variables_set(self):
        return self._image_name and self.__xml_file and self.__scale_factor and self.__min_neighbors
