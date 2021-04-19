import numpy
from SettingWindowHOG import SettingsWindowHOG
from MTCNNDetector import MTCNNFaceDetection
from HOGDetector import HOGFaceDetection
from SettingsWindowOpenCV import SettingsWindowOpenCV
from SettingsWindowsCNN import SettingsWindowCNN
from OpenCVDetector import OpenCVFaceDetection
from CNNDetector import CNNFaceDetection
from pathlib import Path
import cv2
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


class FaceDetection:
    def __init__(self):
        self.__image = NONE
        self.__scale_factor = self.__min_neighbors = self.__min_window_width = self.__min_window_height = \
            self.__max_window_width = self.__max_window_height = self.__pooling_layers = \
            self.__opencv_train_file = self.__cnn_train_file = self.__image_name = self.__upsampling_number = None
        self.__face_found = False

    def open(self):
        self.__init_root()
        self.__init_menu()
        self.__init_picture_box()
        self.__root.mainloop()

    def __opencv_detection(self):
        opencv_detector = OpenCVFaceDetection(self.__image_name, self.__opencv_train_file, self.__scale_factor,
                                              self.__min_neighbors, self.__min_window_width, self.__min_window_height,
                                              self.__max_window_width, self.__max_window_height)
        self.__img, exec_time = opencv_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__img = cv2.cvtColor(self.__img, cv2.COLOR_BGR2RGB)
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __cnn_detection(self):
        cnn_detector = CNNFaceDetection(self.__image_name, self.__cnn_train_file, self.__pooling_layers)
        self.__img, exec_time = cnn_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __hog_detection(self):
        hog_detector = HOGFaceDetection(self.__image_name, self.__upsampling_number)
        self.__img, exec_time = hog_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __mtcnn_detection(self):
        mtcnn_detector = MTCNNFaceDetection(self.__image_name)
        self.__img, exec_time = mtcnn_detector.detect_face()
        if type(self.__img) is numpy.ndarray:
            self.__show_image()
            messagebox.showinfo("Detection time", f"Detection time: {round(exec_time, 6)} seconds")

    def __show_image(self):
        if self.__img.size != 0:
            self.__face_found = True
        self.__image = ImageTk.PhotoImage(Image.fromarray(self.__img))
        self.__picture_box.configure(image=self.__image)
        self.__picture_box.image = self.__image

    def __display_source_image(self):
        self.__image_name = filedialog.askopenfilename(filetypes=[('.jpg files', '*.jpg'), ('.png files', '*.png')])
        if self.__image_name:
            self.__image = Image.open(self.__image_name)
            self.__change_window()
            self.__image = ImageTk.PhotoImage(self.__image)
            self.__picture_box.configure(image=self.__image)
            self.__picture_box.image = self.__image

    def __change_window(self):
        img_width, img_height = self.__image.size
        self.__picture_box.config(width=img_width)
        self.__picture_box.config(height=img_height)
        if img_width > self.__root.winfo_screenwidth() - 40:
            img_width = self.__root.winfo_screenwidth() - 40
        if img_height > self.__root.winfo_screenheight() - 120:
            img_height = self.__root.winfo_screenheight() - 120
        r = (self.__root.winfo_screenwidth() - 20 - (img_width + 25)) / 2
        t = (self.__root.winfo_screenheight() - 90 - (img_height + 25)) / 2
        self.__root.wm_geometry("+%d+%d" % (r, t))
        self.__root.geometry('{}x{}'.format(img_width + 25, img_height + 25))

    def __save_image_as(self):
        if self.__image_correct():
            file_name = filedialog.asksaveasfilename()
            if file_name:
                cv2.imwrite(file_name + Path(self.__image_name).suffix, cv2.cvtColor(self.__img, cv2.COLOR_RGB2BGR))

    def __save_image(self):
        if self.__image_correct():
            cv2.imwrite(self.__image_name, cv2.cvtColor(self.__img, cv2.COLOR_RGB2BGR))

    def __image_correct(self):
        if self.__image != NONE:
            if self.__face_found:
                return True
            else:
                messagebox.showwarning("Save error", "Image hasn't been changed")
        else:
            messagebox.showwarning("Undefined image", "Image hasn't been loaded")
        return False

    def __opencv_settings(self):
        settings_window = SettingsWindowOpenCV(self.__opencv_train_file, self.__scale_factor, self.__min_neighbors
                                               , self.__min_window_width, self.__min_window_height,
                                               self.__max_window_width, self.__max_window_height)
        settings_window.open_dialog(self.__root)
        self.__opencv_train_file = settings_window.xml_file
        self.__scale_factor = settings_window.scale_factor
        self.__min_neighbors = settings_window.min_neighbors
        self.__min_window_height = settings_window.height_min
        self.__min_window_width = settings_window.width_min
        self.__max_window_height = settings_window.height_max
        self.__max_window_width = settings_window.width_max

    def __cnn_settings(self):
        settings_window = SettingsWindowCNN(self.__cnn_train_file, self.__pooling_layers)
        settings_window.open_dialog(self.__root)
        self.__pooling_layers = settings_window.pooling_layers
        self.__cnn_train_file = settings_window.training_file

    def __hog_settings(self):
        settings_window = SettingsWindowHOG(self.__upsampling_number)
        settings_window.open_dialog(self.__root)
        self.__upsampling_number = settings_window.upsampling_number

    def __init_root(self):
        self.__root = Tk()
        self.__root.geometry("500x500")
        self.__root.title("Face detection")
        r = (self.__root.winfo_screenwidth() - self.__root.winfo_reqwidth()) / 2.5
        t = (self.__root.winfo_screenheight() - self.__root.winfo_reqheight()) / 2.5
        self.__root.wm_geometry("+%d+%d" % (r, t))
        # self.__root.resizable(width=False, height=False)
        self.__root.iconphoto(True, ImageTk.PhotoImage(Image.open("app_icon.png")))

    def __init_menu(self):
        self.__menubar = Menu(self.__root)

        self.__file_menu = Menu(self.__menubar, tearoff=0)
        self.__file_menu.add_command(label="Open", command=self.__display_source_image)
        self.__file_menu.add_command(label="Save", command=self.__save_image)
        self.__file_menu.add_command(label="Save as", command=self.__save_image_as)
        self.__menubar.add_cascade(label="File", menu=self.__file_menu)

        self.__menubar.add_separator()

        self.__setting_menu = Menu(self.__menubar, tearoff=0)
        self.__setting_menu.add_command(label="Haar cascade settings", command=self.__opencv_settings)
        self.__setting_menu.add_command(label="CNN settings", command=self.__cnn_settings)
        self.__setting_menu.add_command(label="HOG settings", command=self.__hog_settings)
        self.__menubar.add_cascade(label="Settings", menu=self.__setting_menu)

        self.__menubar.add_separator()

        self.__detect_menu = Menu(self.__menubar, tearoff=0)
        self.__detect_menu.add_command(label="Haar cascade detection", command=self.__opencv_detection)
        self.__detect_menu.add_command(label="CNN detection", command=self.__cnn_detection)
        self.__detect_menu.add_command(label="HOG detection", command=self.__hog_detection)
        self.__detect_menu.add_command(label="MTCNN detection", command=self.__mtcnn_detection)
        self.__menubar.add_cascade(label="Detect", menu=self.__detect_menu)

        self.__root.config(menu=self.__menubar)

    def __init_picture_box(self):
        self.__scrollbarY = ttk.Scrollbar(self.__root, orient=VERTICAL)
        self.__scrollbarY.pack(side=RIGHT, fill=Y)
        self.__scrollbarX = ttk.Scrollbar(self.__root, orient=HORIZONTAL)
        self.__scrollbarX.pack(side=BOTTOM, fill=X)
        self.__my_canvas = Canvas(self.__root)
        self.__my_canvas.pack(side=TOP, fill=BOTH, expand=1)
        self.__scrollbarX.config(command=self.__my_canvas.xview)
        self.__scrollbarY.config(command=self.__my_canvas.yview)

        self.__my_canvas.configure(yscrollcommand=self.__scrollbarY.set, xscrollcommand=self.__scrollbarX.set)
        self.__my_canvas.bind('<Configure>',
                              lambda e: self.__my_canvas.configure(scrollregion=self.__my_canvas.bbox("all")))

        self.__frame = Frame(self.__my_canvas)
        self.__my_canvas.create_window((0, 0), window=self.__frame, anchor="nw")

        self.__picture_box = Label(self.__frame, text="Set the settings and upload an image", font="Arial 16", width=39,
                                   height=15)
        self.__picture_box.pack()


if __name__ == "__main__":
    face_detection = FaceDetection()
    face_detection.open()
