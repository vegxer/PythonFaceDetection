import os.path
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from pathlib import Path
import cv2


class SettingsWindowOpenCV:
    def __init__(self, xml_file, scale_factor, min_neighbors, min_window_width, min_window_height,
                 max_window_width, max_window_height):
        self.xml_file = xml_file
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.width_min = min_window_width
        self.height_min = min_window_height
        self.height_max = max_window_height
        self.width_max = max_window_width

    def open_dialog(self, root):
        self.settings = Toplevel()
        self.settings.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.settings.geometry("420x200")
        self.settings.title("Haar cascade Settings")
        r = (self.settings.winfo_screenwidth() - self.settings.winfo_reqwidth()) / 2.5
        t = (self.settings.winfo_screenheight() - self.settings.winfo_reqheight()) / 2.5
        self.settings.wm_geometry("+%d+%d" % (r, t))
        self.settings.resizable(width=False, height=False)

        Label(self.settings, text="Choose haar cascade file", font="Arial 11").place(x=5, y=0)

        self.list = Combobox(self.settings, value=("...", "Standard haar cascade file", "Choose .xml from computer..."),
                             width=25)
        self.list.bind("<<ComboboxSelected>>", self.__choose_xml)
        self.list.current(0)
        self.list.place(x=180, y=3)

        Label(self.settings, text="Input scale factor (from 1.001 to 2)", font="Arial 11").place(x=5, y=30)
        self.text_scale = Text(self.settings, width=5, height=1)
        self.text_scale.place(x=235, y=33)

        Label(self.settings, text="Input minimum number of neighbors (from 1 to 1000)",
              font="Arial 11").place(x=5, y=60)
        self.text_neighbors = Text(self.settings, width=5, height=1)
        self.text_neighbors.place(x=355, y=63)

        Label(self.settings, text="Input maximum window size (WIDTHxHEIGHT)", font="Arial 11",
              anchor=CENTER).place(x=5, y=90)
        self.text_max_size = Text(self.settings, width=10, height=1)
        self.text_max_size.place(x=320, y=93)

        Label(self.settings, text="Input minimum window size (WIDTHxHEIGHT)", font="Arial 11",
              anchor=CENTER).place(x=5, y=120)
        self.text_min_size = Text(self.settings, width=10, height=1)
        self.text_min_size.place(x=320, y=123)

        self.button_confirm = Button(self.settings, text="Save settings", font="Arial 11", command=self.__save_settings)
        self.button_confirm.place(x=150, y=155)

        self.__set_saved_setting()

        self.settings.transient(root)
        self.settings.grab_set()
        self.settings.mainloop()

    def __set_saved_setting(self):
        if not self.xml_file:
            self.list.current(0)
        elif self.xml_file == cv2.data.haarcascades + "haarcascade_frontalface_alt.xml":
            self.list.current(1)
        else:
            self.list.current(2)
        if self.scale_factor:
            self.text_scale.insert(1.0, str(self.scale_factor))
        if self.min_neighbors:
            self.text_neighbors.insert(1.0, str(self.min_neighbors))
        if self.width_max and self.height_max:
            self.text_max_size.insert(1.0, str(self.width_max) + 'x' + str(self.height_max))
        if self.width_min and self.height_min:
            self.text_min_size.insert(1.0, str(self.width_min) + 'x' + str(self.height_min))

    def __on_closing(self):
        self.settings.grab_release()
        self.settings.quit()
        self.settings.destroy()

    def __choose_xml(self, event):
        if self.list.current() == 2:
            xml_file = filedialog.askopenfilename(filetypes=[('.xml files', '*.xml')])
            if xml_file:
                self.xml_file = xml_file
        elif self.list.current() == 1:
            # if os.path.exists(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"):
            self.xml_file = cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
            # else:
                # messagebox.showerror("File not found", "File \'haarcascade_frontalface_alt.xml\' hasn't been found")

    def __save_settings(self):
        scale_factor_error = self.__save_scale_factor()
        min_neighbors_error = self.__save_min_neighbors()
        min_size_error = self.__save_min_size()
        max_size_error = self.__save_max_size()
        if not (scale_factor_error or min_neighbors_error or min_size_error or max_size_error):
            messagebox.showinfo("Settings save",
                                "Settings have been saved successfully\nYou may close settings window or make changes")
        else:
            messagebox.showinfo("Settings save",
                                "All correct settings are saved\nYou may close settings window or make changes")

    def __save_scale_factor(self):
        try:
            self.scale_factor = float(self.text_scale.get("1.0", END))
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
            self.min_neighbors = int(self.text_neighbors.get("1.0", END))
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
            self.min_size = self.text_min_size.get("1.0", END)
            self.width_min = self.height_min = None
            if self.min_size != '\n':
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
            self.max_size = self.text_max_size.get("1.0", END)
            self.width_max = self.height_max = None
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
