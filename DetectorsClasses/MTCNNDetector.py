import facenet_pytorch
import cv2
import os.path
import torch
from tkinter import messagebox
import time


class MTCNNFaceDetection:
    def __init__(self, image_name):
        self.__img = self.__image_name = None
        self.set_image_path(image_name)

    def detect_face(self):
        end = start = 0
        if self.__are_all_variables_set():
            self.__img = cv2.cvtColor(cv2.imread(self.__image_name), cv2.COLOR_BGR2RGB)
            device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            self.__mtcnn_detector = facenet_pytorch.MTCNN(keep_all=True, device=device)
            start = time.time()
            faces, _ = self.__mtcnn_detector.detect(self.__img)
            end = time.time()
            if faces is not None:
                for face in faces:
                    cv2.rectangle(self.__img, (face[0], face[1]), (face[2], face[3]), (255, 0, 0), 1)
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

    def __are_all_variables_set(self):
        return self.__image_name
