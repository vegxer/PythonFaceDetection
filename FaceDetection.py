from DetectorsClasses.MTCNNDetector import MTCNNFaceDetection
from DetectorsClasses.HOGDetector import HOGFaceDetection
from DetectorsClasses.HaarCascadeDetector import HaarCascadeFaceDetection
from DetectorsClasses.CNNDetector import CNNFaceDetection
from SettingsWindows.SettingsWindowHOG import SettingsWindowHOG
from SettingsWindows.SettingsWindowHaarCascade import SettingsWindowHaarCascade
from SettingsWindows.SettingsWindowCNN import SettingsWindowCNN
from SaveImage import SaveImage
from MainWindowDesigner import MainWindow
import numpy
import cv2
import tkinter
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


# основной класс, управляющий программой
class FaceDetection:
    def __init__(self):
        # создание основного окна
        self.__graphics = MainWindow()
        # объявление переменных изображений, форм и детекторов
        self.__image = tkinter.NONE
        self.__img = self.__image_name = self.__cnn_settings_form = self.__hog_settings_form = \
            self.__haar_settings_form = self.__haar_detector = self.__cnn_detector = self.__hog_detector = \
            self.__mtcnn_detector = None
        self.__face_found = False

    # инициализация интерфейса
    def open(self):
        self.__graphics.init_root()
        # передача методов как параметров для установки обработчиков события нажатия на пункты меню
        self.__graphics.init_menu(self.__display_source_image, self.__save_image, self.__save_image_as,
                                  self.__haar_cascade_settings, self.__cnn_settings, self.__hog_settings,
                                  self.__haar_cascade_detection, self.__cnn_detection, self.__hog_detection,
                                  self.__mtcnn_detection)
        self.__graphics.init_picture_box()
        self.__graphics.window.mainloop()

    # обработчик события нажатия на кнопку "Haar cascade detection"
    def __haar_cascade_detection(self):
        # если форма настроек не была открыта
        if self.__haar_settings_form == None:
            messagebox.showerror("Settings error", "Settings are not set")
        else:
            # передача сохранённых настроек метода
            self.__haar_detector = HaarCascadeFaceDetection(self.__image_name, self.__haar_settings_form.xml_file,
                                                            self.__haar_settings_form.scale_factor,
                                                            self.__haar_settings_form.min_neighbors,
                                                            self.__haar_settings_form.width_min,
                                                            self.__haar_settings_form.height_min,
                                                            self.__haar_settings_form.width_max,
                                                            self.__haar_settings_form.height_max)
            # метод обнаружения лиц (возвращает обработанное изображение и время выполнения)
            self.__img, exec_time = self.__haar_detector.detect_face()
            if type(self.__img) is numpy.ndarray:
                # вывод изображения с обнаруженными лицами на основное окно
                # преобразование цвета
                self.__img = cv2.cvtColor(self.__img, cv2.COLOR_BGR2RGB)
                self.__show_image()
                messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    # обработчик события нажатия на кнопку "CNN detection"
    def __cnn_detection(self):
        # если форма настроек не была открыта
        if self.__cnn_settings_form == None:
            messagebox.showerror("Settings error", "Settings are not set")
        else:
            # передача сохранённых настроек метода
            self.__cnn_detector = CNNFaceDetection(self.__image_name, self.__cnn_settings_form.training_file,
                                                   self.__cnn_settings_form.pooling_layers)
            self.__img, exec_time = self.__cnn_detector.detect_face()
            if type(self.__img) is numpy.ndarray:
                # вывод изображения с обнаруженными лицами на основное окно
                self.__show_image()
                messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    # обработчик события нажатия на кнопку "HOG detection"
    def __hog_detection(self):
        # если форма настроек не была открыта
        if self.__hog_settings_form == None:
            messagebox.showerror("Settings error", "Settings are not set")
        else:
            # передача сохранённых настроек метода
            self.__hog_detector = HOGFaceDetection(self.__image_name, self.__hog_settings_form.upsampling_number)
            self.__img, exec_time = self.__hog_detector.detect_face()
            if type(self.__img) is numpy.ndarray:
                # вывод изображения с обнаруженными лицами на основное окно
                self.__show_image()
                messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    # обработчик события нажатия на кнопку "MTCNN detection"
    def __mtcnn_detection(self):
        self.__mtcnn_detector = MTCNNFaceDetection(self.__image_name)
        self.__img, exec_time = self.__mtcnn_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            # вывод изображения с обнаруженными лицами на основное окно
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    # вывести изображение с обнаруженными лицами
    def __show_image(self):
        if self.__img.size != 0:
            self.__face_found = True
        # преобразование изображения в PhotoImage
        self.__image = ImageTk.PhotoImage(Image.fromarray(self.__img))
        # сохранение изображения в picture_box
        self.__graphics.picture_box.configure(image=self.__image)
        self.__graphics.picture_box.image = self.__image

    # вывести загруженное пользователем изображение (обработчик события нажатия на кнопку "Open")
    def __display_source_image(self):
        image_name = filedialog.askopenfilename(filetypes=[('.jpg files', '*.jpg'), ('.png files', '*.png')])
        if image_name:
            self.__image_name = image_name
            self.__image = Image.open(self.__image_name)
            self.__change_window()
            self.__image = ImageTk.PhotoImage(self.__image)
            self.__graphics.picture_box.configure(image=self.__image)
            self.__graphics.picture_box.image = self.__image

    # изменить размеры окна и picture_box'а под новое изображение
    def __change_window(self):
        img_width, img_height = self.__image.size
        # изменение размеров picture_box
        self.__graphics.picture_box.config(width=img_width)
        self.__graphics.picture_box.config(height=img_height)
        # если изображение не входит на экран
        if img_width > self.__graphics.window.winfo_screenwidth() - 40:
            img_width = self.__graphics.window.winfo_screenwidth() - 40
        if img_height > self.__graphics.window.winfo_screenheight() - 120:
            img_height = self.__graphics.window.winfo_screenheight() - 120
        r = (self.__graphics.window.winfo_screenwidth() - 20 - (img_width + 25)) / 2
        t = (self.__graphics.window.winfo_screenheight() - 90 - (img_height + 25)) / 2
        # изменение размеров окна
        self.__graphics.window.wm_geometry("+%d+%d" % (r, t))
        self.__graphics.window.geometry('{}x{}'.format(img_width + 25, img_height + 25))

    # сохранение изображения по указанному пути
    def __save_image_as(self):
        SaveImage.save_as(self.__image_name, self.__img, self.__face_found)

    # сохранение изображения по существующему пути
    def __save_image(self):
        SaveImage.save(self.__image_name, self.__img, self.__face_found)

    # обработчик события нажатия на кнопку "Haar cascade settings", открывает окно настроек
    def __haar_cascade_settings(self):
        # если окно ещё не создано, то создать его
        if self.__haar_settings_form == None:
            self.__haar_settings_form = SettingsWindowHaarCascade()
        # открыть окно настроек поверх основного окна
        self.__haar_settings_form.open_dialog(self.__graphics.window)

    # обработчик события нажатия на кнопку "CNN settings", открывает окно настроек
    def __cnn_settings(self):
        # если окно ещё не создано, то создать его
        if self.__cnn_settings_form == None:
            self.__cnn_settings_form = SettingsWindowCNN()
        self.__cnn_settings_form.open_dialog(self.__graphics.window)

    # обработчик события нажатия на кнопку "HOG settings", открывает окно настроек
    def __hog_settings(self):
        # если окно ещё не создано, то создать его
        if self.__hog_settings_form == None:
            self.__hog_settings_form = SettingsWindowHOG()
        self.__hog_settings_form.open_dialog(self.__graphics.window)
