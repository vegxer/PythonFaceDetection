from DetectorsClasses.MTCNNDetector import MTCNNFaceDetection
from DetectorsClasses.HOGDetector import HOGFaceDetection
from DetectorsClasses.OpenCVDetector import OpenCVFaceDetection
from DetectorsClasses.CNNDetector import CNNFaceDetection
from SettingsWindows.SettingsWindowHOG import SettingsWindowHOG
from SettingsWindows.SettingsWindowOpenCV import SettingsWindowOpenCV
from SettingsWindows.SettingsWindowCNN import SettingsWindowCNN
from SaveImage import SaveImage
from MainWindowDesigner import MainWindow
import numpy
import cv2
import tkinter
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


class FaceDetection:
    def __init__(self):
        self.__graphics = MainWindow()
        self.__image = tkinter.NONE
        self.__img = self.__image_name = self.__cnn_settings = self.__hog_settings = self.__haar_settings =\
            self.__opencv_detector = self.__cnn_detector = self.__hog_detector = self.__mtcnn_detector = None
        self.__face_found = False

    def open(self):
        self.__graphics.init_root()
        self.__graphics.init_menu(self.__display_source_image, self.__save_image, self.__save_image_as,
                                  self.__opencv_settings, self.__cnn_settings, self.__hog_settings,
                                  self.__opencv_detection, self.__cnn_detection, self.__hog_detection,
                                  self.__mtcnn_detection)
        self.__graphics.init_picture_box()
        self.__graphics.window.mainloop()

    def __opencv_detection(self):
        if self.__haar_settings == None:
            messagebox.showerror("Settings error", "Settings are not set")
        else:
            self.__opencv_detector = OpenCVFaceDetection(self.__image_name, self.__haar_settings.xml_file, self.__haar_settings.scale_factor,
                                                        self.__haar_settings.min_neighbors, self.__haar_settings.width_min, self.__haar_settings.height_min
                                                         , self.__haar_settings.width_max, self.__haar_settings.height_max)
            self.__img, exec_time = self.__opencv_detector.detect_face()
            if type(self.__img) is numpy.ndarray:
                self.__img = cv2.cvtColor(self.__img, cv2.COLOR_BGR2RGB)
                self.__show_image()
                messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __cnn_detection(self):
        if self.__cnn_settings == None:
            messagebox.showerror("Settings error", "Settings are not set")
        else:
            self.__cnn_detector = CNNFaceDetection(self.__image_name, self.__cnn_settings.training_file, self.__cnn_settings.pooling_layers)
            self.__img, exec_time = self.__cnn_detector.detect_face()
            if type(self.__img) is numpy.ndarray:
                self.__show_image()
                messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __hog_detection(self):
        if self.__hog_settings == None:
            messagebox.showerror("Settings error", "Settings are not set")
        else:
            self.__hog_detector = HOGFaceDetection(self.__image_name, self.__hog_settings.upsampling_number)
            self.__img, exec_time = self.__hog_detector.detect_face()
            if type(self.__img) is numpy.ndarray:
                self.__show_image()
                messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __mtcnn_detection(self):
        self.__mtcnn_detector = MTCNNFaceDetection(self.__image_name)
        self.__img, exec_time = self.__mtcnn_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __show_image(self):
        if self.__img.size != 0:
            self.__face_found = True
        self.__image = ImageTk.PhotoImage(Image.fromarray(self.__img))
        self.__graphics.picture_box.configure(image=self.__image)
        self.__graphics.picture_box.image = self.__image

    def __display_source_image(self):
        image_name = filedialog.askopenfilename(filetypes=[('.jpg files', '*.jpg'), ('.png files', '*.png')])
        if image_name:
            self.__image_name = image_name
            self.__image = Image.open(self.__image_name)
            self.__change_window()
            self.__image = ImageTk.PhotoImage(self.__image)
            self.__graphics.picture_box.configure(image=self.__image)
            self.__graphics.picture_box.image = self.__image

    def __change_window(self):
        img_width, img_height = self.__image.size
        self.__graphics.picture_box.config(width=img_width)
        self.__graphics.picture_box.config(height=img_height)
        if img_width > self.__graphics.window.winfo_screenwidth() - 40:
            img_width = self.__graphics.window.winfo_screenwidth() - 40
        if img_height > self.__graphics.window.winfo_screenheight() - 120:
            img_height = self.__graphics.window.winfo_screenheight() - 120
        r = (self.__graphics.window.winfo_screenwidth() - 20 - (img_width + 25)) / 2
        t = (self.__graphics.window.winfo_screenheight() - 90 - (img_height + 25)) / 2
        self.__graphics.window.wm_geometry("+%d+%d" % (r, t))
        self.__graphics.window.geometry('{}x{}'.format(img_width + 25, img_height + 25))

    def __save_image_as(self):
        SaveImage.save_as(self.__image_name, self.__img, self.__face_found)

    def __save_image(self):
        SaveImage.save(self.__image_name, self.__img, self.__face_found)

    def __opencv_settings(self):
        if self.__haar_settings == None:
            self.__haar_settings = SettingsWindowOpenCV()
        self.__haar_settings.open_dialog(self.__graphics.window)

    def __cnn_settings(self):
        if self.__cnn_settings == None:
            self.__cnn_settings = SettingsWindowCNN()
        self.__cnn_settings.open_dialog(self.__graphics.window)

    def __hog_settings(self):
        if self.__hog_settings == None:
            self.__hog_settings = SettingsWindowHOG()
        self.__hog_settings.open_dialog(self.__graphics.window)
