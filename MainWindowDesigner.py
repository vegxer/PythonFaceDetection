from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path


class MainWindow:

    def init_root(self):
        self.window = Tk()
        self.window.geometry("793x409")
        self.window.title("Face detection")
        r = (self.window.winfo_screenwidth() - 768) / 2
        t = (self.window.winfo_screenheight() - 384) / 2
        self.window.wm_geometry("+%d+%d" % (r, t))
        # self.__root.resizable(width=False, height=False)
        self.window.iconphoto(True, ImageTk.PhotoImage(Image.open(str(Path.cwd()) + "\\Images\\app_icon.png")))

    def init_menu(self, display_source_image, save_image, save_image_as, opencv_settings, cnn_settings,
                  hog_settings, opencv_detection, cnn_detection, hog_detection, mtcnn_detection):
        self.__menubar = Menu(self.window)

        self.__file_menu = Menu(self.__menubar, tearoff=0)
        self.__file_menu.add_command(label="Open", command=display_source_image)
        self.__file_menu.add_command(label="Save", command=save_image)
        self.__file_menu.add_command(label="Save as", command=save_image_as)
        self.__menubar.add_cascade(label="File", menu=self.__file_menu)

        self.__menubar.add_separator()

        self.__setting_menu = Menu(self.__menubar, tearoff=0)
        self.__setting_menu.add_command(label="Haar cascade settings", command=opencv_settings)
        self.__setting_menu.add_command(label="CNN settings", command=cnn_settings)
        self.__setting_menu.add_command(label="HOG settings", command=hog_settings)
        self.__menubar.add_cascade(label="Settings", menu=self.__setting_menu)

        self.__menubar.add_separator()

        self.__detect_menu = Menu(self.__menubar, tearoff=0)
        self.__detect_menu.add_command(label="Haar cascade detection", command=opencv_detection)
        self.__detect_menu.add_command(label="CNN detection", command=cnn_detection)
        self.__detect_menu.add_command(label="HOG detection", command=hog_detection)
        self.__detect_menu.add_command(label="MTCNN detection", command=mtcnn_detection)
        self.__menubar.add_cascade(label="Detect", menu=self.__detect_menu)

        self.window.config(menu=self.__menubar)

    def init_picture_box(self):
        self.__scrollbarY = ttk.Scrollbar(self.window, orient=VERTICAL)
        self.__scrollbarY.pack(side=RIGHT, fill=Y)
        self.__scrollbarX = ttk.Scrollbar(self.window, orient=HORIZONTAL)
        self.__scrollbarX.pack(side=BOTTOM, fill=X)
        self.__my_canvas = Canvas(self.window)
        self.__my_canvas.pack(side=TOP, fill=BOTH, expand=1)
        self.__scrollbarX.config(command=self.__my_canvas.xview)
        self.__scrollbarY.config(command=self.__my_canvas.yview)

        self.__my_canvas.configure(yscrollcommand=self.__scrollbarY.set, xscrollcommand=self.__scrollbarX.set)
        self.__my_canvas.bind('<Configure>',
                              lambda e: self.__my_canvas.configure(scrollregion=self.__my_canvas.bbox("all")))

        self.__frame = Frame(self.__my_canvas)
        self.__my_canvas.create_window((0, 0), window=self.__frame, anchor="nw")
        self.__start_image = ImageTk.PhotoImage(Image.open(str(Path.cwd()) + "\\Images\\load_screen.png"))
        self.picture_box = Label(self.__frame, image=self.__start_image)
        self.picture_box.pack()
