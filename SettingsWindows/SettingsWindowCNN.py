import tkinter
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import pathlib
from SettingsWindows.SettingsWindow import SettingsWindow


# класс, создающий и управляющий окном настроек для метода CNN
class SettingsWindowCNN(SettingsWindow):
    def __init__(self, training_file=None, pooling_layers=None):
        self.training_file = training_file
        self.pooling_layers = pooling_layers

    # создание окна
    def open_dialog(self, root):
        super()._init_window()
        # событие на закрытие окна
        self._settings.protocol("WM_DELETE_WINDOW", super()._on_closing)
        self._settings.geometry("400x100")
        self._settings.title("CNN Settings")
        r = (self._settings.winfo_screenwidth() - self._settings.winfo_reqwidth()) / 2.5
        t = (self._settings.winfo_screenheight() - self._settings.winfo_reqheight()) / 2.5
        self._settings.wm_geometry("+%d+%d" % (r, t))
        self._settings.resizable(width=False, height=False)

        tkinter.Label(self._settings, text="Choose CNN weights file", font="Arial 11").place(x=5, y=0)

        self.__list = ttk.Combobox(self._settings, value=("...", "Standard CNN file", "Choose .dat from computer..."),
                                   width=25)
        # установка обработчика события
        self.__list.bind("<<ComboboxSelected>>", self.__save_training_file)
        self.__list.current(0)
        self.__list.place(x=180, y=3)

        tkinter.Label(self._settings, text="Input number of pooling layers (from 0 to 3)", font="Arial 11").place(x=5,
                                                                                                                  y=30)
        self.__text_scale = tkinter.Text(self._settings, width=5, height=1)
        self.__text_scale.place(x=295, y=33)

        self._button_confirm.place(x=150, y=63)

        self._set_saved_settings()

        self._settings.transient(root)
        self._settings.grab_set()
        self._settings.mainloop()

    # обработчик события выбора из списка комбобокса
    def __save_training_file(self, event):
        # выбор файла с компьютера
        if self.__list.current() == 2:
            training_file = filedialog.askopenfilename(filetypes=[('.dat files', '*.dat')])
            if training_file:
                self.training_file = training_file
        # выбор стандартного файла
        elif self.__list.current() == 1:
            if os.path.exists("Training_files\\mmod_human_face_detector.dat"):
                self.training_file = "Training_files\\mmod_human_face_detector.dat"
            else:
                messagebox.showerror("File not found",
                                     f"File \'{str(pathlib.Path.cwd())}\\Training_files"
                                     f"\\mmod_human_face_detector.dat\' hasn't been found")

    # выставление сохранённых настроек, оставшихся с прошлого открытия окна
    def _set_saved_settings(self):
        if not self.training_file:
            self.__list.current(0)
        elif self.training_file == "Training_files\\mmod_human_face_detector.dat":
            self.__list.current(1)
        else:
            self.__list.current(2)

        if self.pooling_layers != None:
            self.__text_scale.insert(1.0, str(self.pooling_layers))

    # сохранение настроек
    def _save_settings(self):
        try:
            # если pooling_layers - целое число
            self.pooling_layers = int(self.__text_scale.get("1.0", tkinter.END))
            if self.pooling_layers < 0 or self.pooling_layers > 3:
                messagebox.showerror("Pooling layers error", "Argument \'Scale factor\' is out of range")
                self.pooling_layers = None
            else:
                messagebox.showinfo("Settings save",
                                    "Settings are saved successfully\nYou may close settings window or make changes")
        except:
            messagebox.showerror("Pooling layers error", "Incorrect pooling layers input")
            self.pooling_layers = None
