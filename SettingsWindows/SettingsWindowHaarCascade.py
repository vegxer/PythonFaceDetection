import tkinter
from tkinter import filedialog, messagebox
from tkinter import ttk
from SettingsWindows.SettingsWindow import SettingsWindow


# класс, создающий и управляющий окном настроек для метода Виолы-Джонса
class SettingsWindowHaarCascade(SettingsWindow):
    def __init__(self, xml_file=None, scale_factor=None, min_neighbors=None, min_window_width=None,
                 min_window_height=None, max_window_width=None, max_window_height=None):
        self.xml_file = xml_file
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.width_min = min_window_width
        self.height_min = min_window_height
        self.height_max = max_window_height
        self.width_max = max_window_width

    # создание окна
    def open_dialog(self, root):
        super()._init_window()
        # событие на закрытие окна
        self._settings.protocol("WM_DELETE_WINDOW", super()._on_closing)
        self._settings.geometry("420x200")
        self._settings.title("Haar cascade Settings")
        r = (self._settings.winfo_screenwidth() - 420) / 2
        t = (self._settings.winfo_screenheight() - 200) / 2
        self._settings.wm_geometry("+%d+%d" % (r, t))
        self._settings.resizable(width=False, height=False)

        tkinter.Label(self._settings, text="Choose haar cascade file", font="Arial 11").place(x=5, y=0)

        self.__list = ttk.Combobox(self._settings,
                                   value=("...", "Standard haar cascade file", "Choose .xml from computer..."),
                                   width=25)
        # установка обработчика события
        self.__list.bind("<<ComboboxSelected>>", self.__choose_xml)
        self.__list.current(0)
        self.__list.place(x=180, y=3)

        tkinter.Label(self._settings, text="Input scale factor (from 1.001 to 2)", font="Arial 11").place(x=5, y=30)
        self.__text_scale = tkinter.Text(self._settings, width=5, height=1)
        self.__text_scale.place(x=235, y=33)

        tkinter.Label(self._settings, text="Input minimum number of neighbors (from 1 to 1000)",
                      font="Arial 11").place(x=5, y=60)
        self.__text_neighbors = tkinter.Text(self._settings, width=5, height=1)
        self.__text_neighbors.place(x=355, y=63)

        tkinter.Label(self._settings, text="Input maximum window size (WIDTHxHEIGHT)", font="Arial 11",
                      anchor=tkinter.CENTER).place(x=5, y=90)
        self.__text_max_size = tkinter.Text(self._settings, width=10, height=1)
        self.__text_max_size.place(x=320, y=93)

        tkinter.Label(self._settings, text="Input minimum window size (WIDTHxHEIGHT)", font="Arial 11",
                      anchor=tkinter.CENTER).place(x=5, y=120)
        self.__text_min_size = tkinter.Text(self._settings, width=10, height=1)
        self.__text_min_size.place(x=320, y=123)

        self._button_confirm.place(x=150, y=155)

        self._set_saved_settings()

        self._settings.transient(root)
        self._settings.grab_set()
        self._settings.mainloop()

    # выставление сохранённых настроек, оставшихся с прошлого открытия окна
    def _set_saved_settings(self):
        if not self.xml_file:
            self.__list.current(0)
        elif self.xml_file == "Training_files\\haarcascade_frontalface_alt.xml":
            self.__list.current(1)
        else:
            self.__list.current(2)
        if self.scale_factor:
            self.__text_scale.insert(1.0, str(self.scale_factor))
        if self.min_neighbors:
            self.__text_neighbors.insert(1.0, str(self.min_neighbors))
        if self.width_max and self.height_max:
            self.__text_max_size.insert(1.0, str(self.width_max) + 'x' + str(self.height_max))
        if self.width_min and self.height_min:
            self.__text_min_size.insert(1.0, str(self.width_min) + 'x' + str(self.height_min))

    # обработчик события выбора из списка комбобокса
    def __choose_xml(self, event):
        # выбор файла с компьютера
        if self.__list.current() == 2:
            xml_file = filedialog.askopenfilename(filetypes=[('.xml files', '*.xml')])
            if xml_file:
                self.xml_file = xml_file
        # выбор стандартного файла
        elif self.__list.current() == 1:
            self.xml_file = "Training_files\\haarcascade_frontalface_alt.xml"

    # сохранение настроек
    def _save_settings(self):
        # ошибки при сохранение настроек
        scale_factor_error = self.__save_scale_factor()
        min_neighbors_error = self.__save_min_neighbors()
        min_size_error = self.__save_min_size()
        max_size_error = self.__save_max_size()
        # если ошибок нет
        if not (scale_factor_error or min_neighbors_error or min_size_error or max_size_error):
            messagebox.showinfo("Settings save",
                                "Settings have been saved successfully\nYou may close settings window or make changes")
        # если есть хотя бы одна ошибка
        else:
            messagebox.showinfo("Settings save",
                                "All correct settings are saved\nYou may close settings window or make changes")

    def __save_scale_factor(self):
        try:
            # если scale_factor - целое число
            self.scale_factor = float(self.__text_scale.get("1.0", tkinter.END))
            if self.scale_factor < 1.001 or self.scale_factor > 2:
                messagebox.showerror("Scale factor error", "Argument \'Scale factor\' is out of range")
                self.scale_factor = None
                return True
            return False
        except:
            messagebox.showerror("Scale factor error", "Incorrect scale factor input")
            self.scale_factor = None
            return True

    def __save_min_neighbors(self):
        try:
            # min_neighbors - целое число
            self.min_neighbors = int(self.__text_neighbors.get("1.0", tkinter.END))
            if (int(self.min_neighbors) != float(self.min_neighbors) or self.min_neighbors < 1
                    or self.min_neighbors > 1000):
                messagebox.showerror("Minimum neighbors number error",
                                     "Argument \'Minimum number of neighbors\' is out of range")
                self.min_neighbors = None
                return True
            return False
        except:
            messagebox.showerror("Minimum neighbors number error", "Incorrect minimum neighbors number input")
            self.min_neighbors = None
            return True

    def __save_min_size(self):
        try:
            self.min_size = self.__text_min_size.get("1.0", tkinter.END)
            self.width_min = self.height_min = None
            # если поле не пустое
            if self.min_size != '\n':
                # если в размере есть символ 'x'
                if 'x' in self.min_size:
                    self.width_min = int(self.min_size[0:self.min_size.find('x')])
                    self.height_min = int(self.min_size[self.min_size.find('x') + 1:])
                    if self.width_min < 1 or self.height_min < 1:
                        raise ValueError
                else:
                    raise ValueError
            return False
        except ValueError:
            messagebox.showerror("Incorrect size input", "Incorrect minimum window size input")
            self.width_min = self.height_min = None
            return True

    def __save_max_size(self):
        try:
            self.max_size = self.__text_max_size.get("1.0", tkinter.END)
            self.width_max = self.height_max = None
            # если поле не пустое
            if self.max_size != '\n':
                if 'x' in self.max_size:
                    self.width_max = int(self.max_size[0:self.max_size.find('x')])
                    self.height_max = int(self.max_size[self.max_size.find('x') + 1:])
                    if self.width_max < self.width_min and self.height_max < self.height_min:
                        raise ValueError
                else:
                    raise ValueError
            return False
        except ValueError:
            messagebox.showerror("Incorrect size input", "Incorrect maximum window size input")
            self.width_max = self.height_max = None
            return True
