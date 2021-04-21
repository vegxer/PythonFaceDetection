from SettingWindowHOG import SettingsWindowHOG
from MTCNNDetector import MTCNNFaceDetection
from HOGDetector import HOGFaceDetection
from SettingsWindowOpenCV import SettingsWindowOpenCV
from SettingsWindowsCNN import SettingsWindowCNN
from OpenCVDetector import OpenCVFaceDetection
from CNNDetector import CNNFaceDetection
from SaveImage import SaveImage
from MainWindowDesigner import MainWindow
import numpy
import cv2
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


class FaceDetection:
    def __init__(self):
        self.graphics = MainWindow(self)
        self.__image = NONE
        self.__scale_factor = self.__min_neighbors = self.__min_window_width = self.__min_window_height = \
            self.__max_window_width = self.__max_window_height = self.__pooling_layers = self.__img = \
            self.__opencv_train_file = self.__cnn_train_file = self.__image_name = self.__upsampling_number = None
        self.__face_found = False

    def open(self):
        self.graphics.init_root()
        self.graphics.init_menu()
        self.graphics.init_picture_box()
        self.graphics.window.mainloop()

    def opencv_detection(self):
        opencv_detector = OpenCVFaceDetection(self.__image_name, self.__opencv_train_file, self.__scale_factor,
                                              self.__min_neighbors, self.__min_window_width, self.__min_window_height,
                                              self.__max_window_width, self.__max_window_height)
        self.__img, exec_time = opencv_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__img = cv2.cvtColor(self.__img, cv2.COLOR_BGR2RGB)
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def cnn_detection(self):
        cnn_detector = CNNFaceDetection(self.__image_name, self.__cnn_train_file, self.__pooling_layers)
        self.__img, exec_time = cnn_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def hog_detection(self):
        hog_detector = HOGFaceDetection(self.__image_name, self.__upsampling_number)
        self.__img, exec_time = hog_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def mtcnn_detection(self):
        mtcnn_detector = MTCNNFaceDetection(self.__image_name)
        self.__img, exec_time = mtcnn_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __show_image(self):
        if self.__img.size != 0:
            self.__face_found = True
        self.__image = ImageTk.PhotoImage(Image.fromarray(self.__img))
        self.graphics.picture_box.configure(image=self.__image)
        self.graphics.picture_box.image = self.__image

    def display_source_image(self):
        self.__image_name = filedialog.askopenfilename(filetypes=[('.jpg files', '*.jpg'), ('.png files', '*.png')])
        if self.__image_name:
            self.__image = Image.open(self.__image_name)
            self.__change_window()
            self.__image = ImageTk.PhotoImage(self.__image)
            self.graphics.picture_box.configure(image=self.__image)
            self.graphics.picture_box.image = self.__image

    def __change_window(self):
        img_width, img_height = self.__image.size
        self.graphics.picture_box.config(width=img_width)
        self.graphics.picture_box.config(height=img_height)
        if img_width > self.graphics.window.winfo_screenwidth() - 40:
            img_width = self.graphics.window.winfo_screenwidth() - 40
        if img_height > self.graphics.window.winfo_screenheight() - 120:
            img_height = self.graphics.window.winfo_screenheight() - 120
        r = (self.graphics.window.winfo_screenwidth() - 20 - (img_width + 25)) / 2
        t = (self.graphics.window.winfo_screenheight() - 90 - (img_height + 25)) / 2
        self.graphics.window.wm_geometry("+%d+%d" % (r, t))
        self.graphics.window.geometry('{}x{}'.format(img_width + 25, img_height + 25))

    def save_image_as(self):
        SaveImage.save_as(self.__image_name, self.__img, self.__face_found)

    def save_image(self):
        SaveImage.save(self.__image_name, self.__img, self.__face_found)

    def opencv_settings(self):
        settings_window = SettingsWindowOpenCV(self.__opencv_train_file, self.__scale_factor, self.__min_neighbors
                                               , self.__min_window_width, self.__min_window_height,
                                               self.__max_window_width, self.__max_window_height)
        settings_window.open_dialog(self.graphics)
        self.__opencv_train_file = settings_window.xml_file
        self.__scale_factor = settings_window.scale_factor
        self.__min_neighbors = settings_window.min_neighbors
        self.__min_window_height = settings_window.height_min
        self.__min_window_width = settings_window.width_min
        self.__max_window_height = settings_window.height_max
        self.__max_window_width = settings_window.width_max

    def cnn_settings(self):
        settings_window = SettingsWindowCNN(self.__cnn_train_file, self.__pooling_layers)
        settings_window.open_dialog(self.graphics)
        self.__pooling_layers = settings_window.pooling_layers
        self.__cnn_train_file = settings_window.training_file

    def hog_settings(self):
        settings_window = SettingsWindowHOG(self.__upsampling_number)
        settings_window.open_dialog(self.graphics)
        self.__upsampling_number = settings_window.upsampling_number
