import facenet_pytorch
import cv2
from tkinter import messagebox
import time
from DetectorsClasses.Detector import Detector


# класс для обнаружения лиц методом MTCNN
class MTCNNFaceDetection(Detector):
    def __init__(self, image_name):
        super().__init__(image_name)
        super().set_image_path(image_name)

    # обнаруживает лица на изображении, возвращает изображение и время выполнения
    def detect_face(self):
        img = None
        end = start = 0
        if self._are_all_variables_set():
            # загрузка изображения
            img = cv2.cvtColor(cv2.imread(self._image_name), cv2.COLOR_BGR2RGB)
            self.__mtcnn_detector = facenet_pytorch.MTCNN(keep_all=True, device='cpu')
            # замер времени выполнения алгоритма
            start = time.time()
            faces, _ = self.__mtcnn_detector.detect(img)
            end = time.time()
            # рисует прямоугольники вокруг лиц
            if faces is not None:
                for face in faces:
                    cv2.rectangle(img, (face[0], face[1]), (face[2], face[3]), (255, 0, 0), 1)
        else:
            messagebox.showerror("Settings error", "Detection is not available due to settings")
        return img, end - start

    def _are_all_variables_set(self):
        return self._image_name
