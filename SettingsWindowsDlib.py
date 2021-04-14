from tkinter.ttk import Combobox
from tkinter import *
from tkinter import messagebox, filedialog
import os.path


class SettingsWindowDlib:
    def __init__(self, training_file, pooling_layers):
        self.training_file = training_file
        self.pooling_layers = pooling_layers

    def open_dialog(self, root):
        self.settings = Toplevel()
        self.settings.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.settings.geometry("400x100")
        self.settings.title("CNN Settings")
        r = (self.settings.winfo_screenwidth() - self.settings.winfo_reqwidth()) / 2.5
        t = (self.settings.winfo_screenheight() - self.settings.winfo_reqheight()) / 2.5
        self.settings.wm_geometry("+%d+%d" % (r, t))
        self.settings.resizable(width=False, height=False)

        Label(self.settings, text="Choose CNN training file", font="Arial 11").place(x=5, y=0)

        self.list = Combobox(self.settings, value=("...", "Standard CNN file", "Choose .dat from computer..."),
                             width=25)
        self.list.bind("<<ComboboxSelected>>", self.__save_training_file)
        self.list.current(0)
        self.list.place(x=180, y=3)

        Label(self.settings, text="Input number of pooling layers (from 0 to 3)", font="Arial 11").place(x=5, y=30)
        self.text_scale = Text(self.settings, width=5, height=1)
        self.text_scale.place(x=295, y=33)

        self.button_confirm = Button(self.settings, text="Save settings", font="Arial 11", command=self.__save_settings)
        self.button_confirm.place(x=150, y=63)

        self.__set_saved_setting()

        self.settings.transient(root)
        self.settings.grab_set()
        self.settings.mainloop()

    def __on_closing(self):
        self.settings.grab_release()
        self.settings.quit()
        self.settings.destroy()

    def __save_training_file(self, event):
        if self.list.current() == 2:
            self.training_file = filedialog.askopenfilename(filetypes=[('.dat files', '*.dat')])
        elif self.list.current() == 1:
            if os.path.exists("mmod_human_face_detector.dat"):
                self.training_file = "mmod_human_face_detector.dat"
            else:
                messagebox.showerror("File not found", "File \'mmod_human_face_detector.dat\' hasn't been found")

    def __set_saved_setting(self):
        if not self.training_file:
            self.list.current(0)
        elif self.training_file == "mmod_human_face_detector.dat":
            self.list.current(1)
        else:
            self.list.current(2)

        if self.pooling_layers != None:
            self.text_scale.insert(1.0, str(self.pooling_layers))

    def __save_settings(self):
        try:
            self.pooling_layers = int(self.text_scale.get("1.0", END))
            if self.pooling_layers < 0 or self.pooling_layers > 3:
                messagebox.showerror("Pooling layers error", "Argument \'Scale factor\' is out of range")
                self.pooling_layers = None
            else:
                messagebox.showinfo("Settings save",
                                    "Settings have been saved successfully\nYou may close settings window or make changes")
        except:
            messagebox.showerror("Pooling layers error", "Incorrect pooling layers input")
            self.pooling_layers = None
