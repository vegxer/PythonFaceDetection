from abc import abstractmethod
import os
from tkinter import messagebox


class Detector:

    def __init__(self, image_name):
        self._image_name = image_name

    @abstractmethod
    def detect_face(self):
        pass

    @abstractmethod
    def _are_all_variables_set(self):
        pass

    def get_image_path(self):
        return self._image_name

    def set_image_path(self, path):
        if os.path.exists(str(path)):
            self._image_name = path
        else:
            messagebox.showerror("File error", "Image is not found")
