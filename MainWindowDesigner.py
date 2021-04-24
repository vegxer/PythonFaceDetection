from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path


class MainWindow:
    def __init__(self, parent_class):
        self.parent_class = parent_class

    def init_root(self):
        self.window = Tk()
        self.window.geometry("793x409")
        self.window.title("Face detection")
        r = (self.window.winfo_screenwidth() - 768) / 2
        t = (self.window.winfo_screenheight() - 384) / 2
        self.window.wm_geometry("+%d+%d" % (r, t))
        # self.__root.resizable(width=False, height=False)
        self.window.iconphoto(True, ImageTk.PhotoImage(Image.open(str(Path.cwd()) + "\\Images\\app_icon.png")))

    def init_menu(self):
        self.menubar = Menu(self.window)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.parent_class.display_source_image)
        self.file_menu.add_command(label="Save", command=self.parent_class.save_image)
        self.file_menu.add_command(label="Save as", command=self.parent_class.save_image_as)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.menubar.add_separator()

        self.setting_menu = Menu(self.menubar, tearoff=0)
        self.setting_menu.add_command(label="Haar cascade settings", command=self.parent_class.opencv_settings)
        self.setting_menu.add_command(label="CNN settings", command=self.parent_class.cnn_settings)
        self.setting_menu.add_command(label="HOG settings", command=self.parent_class.hog_settings)
        self.menubar.add_cascade(label="Settings", menu=self.setting_menu)

        self.menubar.add_separator()

        self.detect_menu = Menu(self.menubar, tearoff=0)
        self.detect_menu.add_command(label="Haar cascade detection", command=self.parent_class.opencv_detection)
        self.detect_menu.add_command(label="CNN detection", command=self.parent_class.cnn_detection)
        self.detect_menu.add_command(label="HOG detection", command=self.parent_class.hog_detection)
        self.detect_menu.add_command(label="MTCNN detection", command=self.parent_class.mtcnn_detection)
        self.menubar.add_cascade(label="Detect", menu=self.detect_menu)

        self.window.config(menu=self.menubar)

    def init_picture_box(self):
        self.scrollbarY = ttk.Scrollbar(self.window, orient=VERTICAL)
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        self.scrollbarX = ttk.Scrollbar(self.window, orient=HORIZONTAL)
        self.scrollbarX.pack(side=BOTTOM, fill=X)
        self.my_canvas = Canvas(self.window)
        self.my_canvas.pack(side=TOP, fill=BOTH, expand=1)
        self.scrollbarX.config(command=self.my_canvas.xview)
        self.scrollbarY.config(command=self.my_canvas.yview)

        self.my_canvas.configure(yscrollcommand=self.scrollbarY.set, xscrollcommand=self.scrollbarX.set)
        self.my_canvas.bind('<Configure>',
                            lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

        self.frame = Frame(self.my_canvas)
        self.my_canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.start_image = ImageTk.PhotoImage(Image.open(str(Path.cwd()) + "\\Images\\load_screen.png"))
        self.picture_box = Label(self.frame, image=self.start_image)
        self.picture_box.pack()
