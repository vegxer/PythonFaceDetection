from tkinter.ttk import Combobox
from tkinter import *
from tkinter import messagebox, filedialog
import os.path
from pathlib import Path

class SettingsWindowCNN:
    def __init__(self, training_file, pooling_layers):
        self.training_file = training_file
        self.pooling_layers = pooling_layers

    def open_dialog(self, root):
        self.__settings = Toplevel()
        self.__settings.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__settings.geometry("400x100")
        self.__settings.title("CNN Settings")
        r = (self.__settings.winfo_screenwidth() - self.__settings.winfo_reqwidth()) / 2.5
        t = (self.__settings.winfo_screenheight() - self.__settings.winfo_reqheight()) / 2.5
        self.__settings.wm_geometry("+%d+%d" % (r, t))
        self.__settings.resizable(width=False, height=False)

        Label(self.__settings, text="Choose CNN training file", font="Arial 11").place(x=5, y=0)

        self.__list = Combobox(self.__settings, value=("...", "Standard CNN file", "Choose .dat from computer..."),
                               width=25)
        self.__list.bind("<<ComboboxSelected>>", self.__save_training_file)
        self.__list.current(0)
        self.__list.place(x=180, y=3)

        Label(self.__settings, text="Input number of pooling layers (from 0 to 3)", font="Arial 11").place(x=5, y=30)
        self.__text_scale = Text(self.__settings, width=5, height=1)
        self.__text_scale.place(x=295, y=33)

        self.__button_confirm = Button(self.__settings, text="Save settings", font="Arial 11", command=self.__save_settings)
        self.__button_confirm.place(x=150, y=63)

        self.__set_saved_setting()

        self.__settings.transient(root)
        self.__settings.grab_set()
        self.__settings.mainloop()

    def __on_closing(self):
        self.__settings.grab_release()
        self.__settings.quit()
        self.__settings.destroy()

    def __save_training_file(self, event):
        if self.__list.current() == 2:
            training_file = filedialog.askopenfilename(filetypes=[('.dat files', '*.dat')])
            if training_file:
                self.training_file = training_file
        elif self.__list.current() == 1:
            if os.path.exists("Training_files\\mmod_human_face_detector.dat"):
                self.training_file = "Training_files\\mmod_human_face_detector.dat"
            else:
                messagebox.showerror("File not found", f"File \'{str(Path.cwd())}\\Training_files\\mmod_human_face_detector.dat\' hasn't been found")

    def __set_saved_setting(self):
        if not self.training_file:
            self.__list.current(0)
        elif self.training_file == "Training_files\\mmod_human_face_detector.dat":
            self.__list.current(1)
        else:
            self.__list.current(2)

        if self.pooling_layers != None:
            self.__text_scale.insert(1.0, str(self.pooling_layers))

    def __save_settings(self):
        try:
            self.pooling_layers = int(self.__text_scale.get("1.0", END))
            if self.pooling_layers < 0 or self.pooling_layers > 3:
                messagebox.showerror("Pooling layers error", "Argument \'Scale factor\' is out of range")
                self.pooling_layers = None
            else:
                messagebox.showinfo("Settings save",
                                    "Settings have been saved successfully\nYou may close settings window or make changes")
        except:
            messagebox.showerror("Pooling layers error", "Incorrect pooling layers input")
            self.pooling_layers = None
