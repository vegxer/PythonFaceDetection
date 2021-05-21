import facenet_pytorch
import cv2
import os.path
import torch
from tkinter import messagebox
import time
from DetectorsClasses.Detector import Detector


class MTCNNFaceDetection(Detector):
    def __init__(self, image_name):
        super().__init__(image_name)
        self.set_image_path(image_name)

    def detect_face(self):
        end = start = 0
        if self._are_all_variables_set():
            self._img = cv2.cvtColor(cv2.imread(self._image_name), cv2.COLOR_BGR2RGB)
            device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            self.__mtcnn_detector = facenet_pytorch.MTCNN(keep_all=True, device=device)
            start = time.time()
            faces, _ = self.__mtcnn_detector.detect(self._img)
            end = time.time()
            if faces is not None:
                for face in faces:
                    cv2.rectangle(self._img, (face[0], face[1]), (face[2], face[3]), (255, 0, 0), 1)
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

    def _are_all_variables_set(self):
        return self._image_name
