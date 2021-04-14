import numpy

from SettingsWindowOpenCV import SettingsWindowOpenCV
from SettingsWindowsDlib import SettingsWindowDlib
from OpenCVDetector import OpenCVFaceDetection
from DlibDetector import DlibFaceDetection
from pathlib import Path
import cv2
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


class FaceDetection:
    def __init__(self):
        self.image = NONE
        self.scale_factor = self.min_neighbors = self.min_window_width = self.min_window_height = \
            self.max_window_width = self.max_window_height = self.pooling_layers = \
            self.opencv_train_file = self.dlib_train_file = self.image_name = None
        self.face_found = False

    def open(self):
        self.__init_root()
        self.__init_menu()
        self.__init_picture_box()
        self.root.mainloop()

    def __opencv_detection(self):
        opencv_detector = OpenCVFaceDetection(self.image_name, self.opencv_train_file, self.scale_factor,
                                              self.min_neighbors, self.min_window_width, self.min_window_height,
                                              self.max_window_width, self.max_window_height)
        self.img = opencv_detector.detect_face()
        if type(self.img) is numpy.ndarray:
            self.__show_image()

    def __dlib_detection(self):
        dlib_detector = DlibFaceDetection(self.image_name, self.dlib_train_file, self.pooling_layers)
        self.img = dlib_detector.detect_face()
        if type(self.img) is numpy.ndarray:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
            self.__show_image()

    def __show_image(self):
        if self.img.size != 0:
            self.face_found = True
        self.image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)))
        self.picture_box.configure(image=self.image)
        self.picture_box.image = self.image

    def __display_source_image(self):
        self.image_name = filedialog.askopenfilename(filetypes=[('.jpg files', '*.jpg'), ('.png files', '*.png')])
        if self.image_name:
            self.image = Image.open(self.image_name)
            self.__change_window()
            self.image = ImageTk.PhotoImage(self.image)
            self.picture_box.configure(image=self.image)
            self.picture_box.image = self.image

    def __change_window(self):
        img_width, img_height = self.image.size
        self.picture_box.config(width=img_width)
        self.picture_box.config(height=img_height)
        if img_width > self.root.winfo_screenwidth() - 40:
            img_width = self.root.winfo_screenwidth() - 40
        if img_height > self.root.winfo_screenheight() - 120:
            img_height = self.root.winfo_screenheight() - 120
        r = (self.root.winfo_screenwidth() - 20 - (img_width + 25)) / 2
        t = (self.root.winfo_screenheight() - 90 - (img_height + 25)) / 2
        self.root.wm_geometry("+%d+%d" % (r, t))
        self.root.geometry('{}x{}'.format(img_width + 25, img_height + 25))

    def __save_image_as(self):
        if self.__image_correct():
            file_name = filedialog.asksaveasfilename()
            if file_name:
                cv2.imwrite(file_name + Path(self.image_name).suffix, self.img)

    def __save_image(self):
        if self.__image_correct():
            cv2.imwrite(self.image_name, self.img)

    def __image_correct(self):
        if self.image != NONE:
            if self.face_found:
                return True
            else:
                messagebox.showwarning("Save error", "Image hasn't been changed")
        else:
            messagebox.showwarning("Undefined image", "Image hasn't been loaded")
        return False

    def __opencv_settings(self):
        settings_window = SettingsWindowOpenCV(self.opencv_train_file, self.scale_factor, self.min_neighbors
                                               , self.min_window_width, self.min_window_height,
                                               self.max_window_width, self.max_window_height)
        settings_window.open_dialog(self.root)
        self.opencv_train_file = settings_window.xml_file
        self.scale_factor = settings_window.scale_factor
        self.min_neighbors = settings_window.min_neighbors
        self.min_window_height = settings_window.height_min
        self.min_window_width = settings_window.width_min
        self.max_window_height = settings_window.height_max
        self.max_window_width = settings_window.width_max

    def __dlib_settings(self):
        settings_window = SettingsWindowDlib(self.dlib_train_file, self.pooling_layers)
        settings_window.open_dialog(self.root)
        self.pooling_layers = settings_window.pooling_layers
        self.dlib_train_file = settings_window.training_file

    def __init_root(self):
        self.root = Tk()
        self.root.geometry("500x500")
        self.root.title("Face detection")
        r = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2.5
        t = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2.5
        self.root.wm_geometry("+%d+%d" % (r, t))
        self.root.resizable(width=False, height=False)
        self.root.iconphoto(True, ImageTk.PhotoImage(Image.open("app_icon.png")))

    def __init_menu(self):
        self.menubar = Menu(self.root)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.__display_source_image)
        self.file_menu.add_command(label="Save", command=self.__save_image)
        self.file_menu.add_command(label="Save as", command=self.__save_image_as)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.menubar.add_separator()

        self.setting_menu = Menu(self.menubar, tearoff=0)
        self.setting_menu.add_command(label="Haar cascade setting", command=self.__opencv_settings)
        self.setting_menu.add_command(label="CNN settings", command=self.__dlib_settings)
        self.menubar.add_cascade(label="Settings", menu=self.setting_menu)

        self.menubar.add_separator()

        self.detect_menu = Menu(self.menubar, tearoff=0)
        self.detect_menu.add_command(label="Haar cascade detection", command=self.__opencv_detection)
        self.detect_menu.add_command(label="CNN detection", command=self.__dlib_detection)
        self.menubar.add_cascade(label="Detect", menu=self.detect_menu)

        self.root.config(menu=self.menubar)

    def __init_picture_box(self):
        self.scrollbarY = ttk.Scrollbar(self.root, orient=VERTICAL)
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        self.scrollbarX = ttk.Scrollbar(self.root, orient=HORIZONTAL)
        self.scrollbarX.pack(side=BOTTOM, fill=X)
        self.my_canvas = Canvas(self.root)
        self.my_canvas.pack(side=TOP, fill=BOTH, expand=1)
        self.scrollbarX.config(command=self.my_canvas.xview)
        self.scrollbarY.config(command=self.my_canvas.yview)

        self.my_canvas.configure(yscrollcommand=self.scrollbarY.set, xscrollcommand=self.scrollbarX.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

        self.frame = Frame(self.my_canvas)
        self.my_canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.picture_box = Label(self.frame, text="Set the settings and upload an image", font="Arial 16", width=39,
                                 height=15)
        self.picture_box.pack()


if __name__ == "__main__":
    face_detection = FaceDetection()
    face_detection.open()
