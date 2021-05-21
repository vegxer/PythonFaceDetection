from abc import abstractmethod, abstractproperty


class Detector:

    def __init__(self, image_name):
        self._img = self._face_detector = None
        self._image_name = image_name

    @abstractmethod
    def detect_face(self):
        pass

    @abstractmethod
    def _are_all_variables_set(self):
        pass

    @abstractproperty
    def get_image_path(self):
        pass

    @abstractproperty
    def set_image_path(self, path):
        pass
