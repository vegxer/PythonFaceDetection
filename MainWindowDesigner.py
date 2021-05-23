from tkinter import ttk
import tkinter
from PIL import ImageTk, Image
import pathlib


# класс, создающий главное окно программы
class MainWindow:
    # инициализация окна
    def init_root(self):
        self.window = tkinter.Tk()
        self.window.geometry("793x409")
        self.window.title("Face detection")
        r = (self.window.winfo_screenwidth() - 768) / 2
        t = (self.window.winfo_screenheight() - 384) / 2
        self.window.wm_geometry("+%d+%d" % (r, t))
        self.window.iconphoto(True, ImageTk.PhotoImage(Image.open(str(pathlib.Path.cwd()) + "\\Images\\app_icon.png")))

    # инициализация меню выбора действий
    def init_menu(self, display_source_image, save_image, save_image_as, haar_cascade_settings, cnn_settings,
                  hog_settings, opencv_detection, cnn_detection, hog_detection, mtcnn_detection):
        self.__menubar = tkinter.Menu(self.window)

        # добавление пунктов меню и обработчиков событий к ним
        self.__file_menu = tkinter.Menu(self.__menubar, tearoff=0)
        self.__file_menu.add_command(label="Open", command=display_source_image)
        self.__file_menu.add_command(label="Save", command=save_image)
        self.__file_menu.add_command(label="Save as", command=save_image_as)
        self.__menubar.add_cascade(label="File", menu=self.__file_menu)

        self.__menubar.add_separator()

        self.__setting_menu = tkinter.Menu(self.__menubar, tearoff=0)
        self.__setting_menu.add_command(label="Haar cascade settings", command=haar_cascade_settings)
        self.__setting_menu.add_command(label="CNN settings", command=cnn_settings)
        self.__setting_menu.add_command(label="HOG settings", command=hog_settings)
        self.__menubar.add_cascade(label="Settings", menu=self.__setting_menu)

        self.__menubar.add_separator()

        self.__detect_menu = tkinter.Menu(self.__menubar, tearoff=0)
        self.__detect_menu.add_command(label="Haar cascade detection", command=opencv_detection)
        self.__detect_menu.add_command(label="CNN detection", command=cnn_detection)
        self.__detect_menu.add_command(label="HOG detection", command=hog_detection)
        self.__detect_menu.add_command(label="MTCNN detection", command=mtcnn_detection)
        self.__menubar.add_cascade(label="Detect", menu=self.__detect_menu)

        # добавить к окну меню
        self.window.config(menu=self.__menubar)

    # инициализация контейнера под изображение
    def init_picture_box(self):
        # добавление ползунков по краям окна
        self.__scrollbarY = ttk.Scrollbar(self.window, orient=tkinter.VERTICAL)
        self.__scrollbarY.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.__scrollbarX = ttk.Scrollbar(self.window, orient=tkinter.HORIZONTAL)
        self.__scrollbarX.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.__my_canvas = tkinter.Canvas(self.window)
        self.__my_canvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.__scrollbarX.config(command=self.__my_canvas.xview)
        self.__scrollbarY.config(command=self.__my_canvas.yview)

        self.__my_canvas.configure(yscrollcommand=self.__scrollbarY.set, xscrollcommand=self.__scrollbarX.set)
        self.__my_canvas.bind('<Configure>',
                              lambda e: self.__my_canvas.configure(scrollregion=self.__my_canvas.bbox("all")))

        self.__frame = tkinter.Frame(self.__my_canvas)
        self.__my_canvas.create_window((0, 0), window=self.__frame, anchor="nw")
        self.__start_image = ImageTk.PhotoImage(Image.open(str(pathlib.Path.cwd()) + "\\Images\\load_screen.png"))
        # инициализация контейнера под изображение
        self.picture_box = tkinter.Label(self.__frame, image=self.__start_image)
        self.picture_box.pack()
