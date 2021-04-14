from tkinter import messagebox
import cv2
import os.path


class OpenCVFaceDetection:
    def __init__(self, image_name, xml_file, scale_factor, min_neighbors, min_window_width=None, min_window_height=None,
                 max_window_width=None, max_window_height=None):
        self.__img = None
        self.set_image_path(image_name)
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
        if self.__are_all_variables_set():
            face_cascade = cv2.CascadeClassifier(self.__xml_file)
            self.__img = cv2.imread(self.__image_name)
            gray = cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
            faces = self.__detect_faces(face_cascade, gray)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.__img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        else:
            messagebox.showerror("Settings error", "Not all settings have been set")
        return self.__img

    def __detect_faces(self, face_cascade, gray):
        if self.__min_window_width and self.__max_window_width:
            return face_cascade.detectMultiScale(gray, scaleFactor=self.__scale_factor,
                                                 minNeighbors=self.__min_neighbors,
                                                 minSize=(self.__min_window_width, self.__min_window_height),
                                                 maxSize=(self.__max_window_width, self.__max_window_height))
        elif self.__min_window_width:
            return face_cascade.detectMultiScale(gray, scaleFactor=self.__scale_factor,
                                                 minNeighbors=self.__min_neighbors,
                                                 minSize=(self.__min_window_width, self.__min_window_height))
        elif self.__max_window_width:
            return face_cascade.detectMultiScale(gray, scaleFactor=self.__scale_factor,
                                                 minNeighbors=self.__min_neighbors,
                                                 maxSize=(self.__max_window_width, self.__max_window_height))
        else:
            return face_cascade.detectMultiScale(gray, scaleFactor=self.__scale_factor,
                                                 minNeighbors=self.__min_neighbors)

    def set_image_path(self, path):
        if os.path.exists(path):
            self.__image_name = path
        else:
            raise FileNotFoundError

    def get_image_path(self):
        return self.__image_name

    def set_training_file(self, path):
        if os.path.exists(path):
            self.__xml_file = path
        else:
            raise FileNotFoundError

    def get_training_file(self):
        return self.__xml_file

    def set_scale_factor(self, scale_factor):
        if type(scale_factor) is float:
            if 0.001 <= scale_factor <= 2:
                self.__scale_factor = scale_factor
            else:
                raise ValueError
        else:
            raise TypeError

    def get_scale_factor(self):
        return self.__scale_factor

    def set_min_neighbors(self, min_neighbors):
        if type(min_neighbors) is int:
            if 1000 >= min_neighbors > 0:
                self.__min_neighbors = min_neighbors
            else:
                raise ValueError
        else:
            raise TypeError

    def get_min_neighbors(self):
        return self.__min_neighbors

    def set_min_size(self, size):
        width = size[0:size.find('x')](TypeError)(int)
        height = size[size.find('x') + 1:](TypeError)(int)
        if width < 1 or height < 1 or (self.__max_window_width != None and self.__max_window_height < height and self.__max_window_width < width):
            raise ValueError
        self.__min_window_width = width
        self.__min_window_height = height

    def get_min_size(self):
        return self.__min_window_width, self.__min_window_height

    def set_max_size(self, size):
        width = size[0:size.find('x')](TypeError)(int)
        height = size[size.find('x') + 1:](TypeError)(int)
        if width < 1 or height < 1 or (self.__min_window_width != None and self.__min_window_height > height and self.__min_window_width > width):
            raise ValueError
        self.__max_window_width = width
        self.__max_window_height = height

    def get_max_size(self):
        return self.__max_window_width, self.__max_window_height

    def __are_all_variables_set(self):
        return self.__image_name and self.__xml_file and self.__scale_factor and self.__min_neighbors
