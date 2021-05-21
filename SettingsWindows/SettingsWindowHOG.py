import tkinter
from tkinter import messagebox
from SettingsWindows.SettingsWindow import SettingsWindow


class SettingsWindowHOG(SettingsWindow):
    def __init__(self, upsampling_number=None):
        self.upsampling_number = upsampling_number

    def open_dialog(self, root):
        super()._init_window()
        self._settings.protocol("WM_DELETE_WINDOW", super()._on_closing)
        self._settings.geometry("380x70")
        self._settings.title("HOG Settings")
        r = (self._settings.winfo_screenwidth() - self._settings.winfo_reqwidth()) / 2.5
        t = (self._settings.winfo_screenheight() - self._settings.winfo_reqheight()) / 2.5
        self._settings.wm_geometry("+%d+%d" % (r, t))
        self._settings.resizable(width=False, height=False)

        tkinter.Label(self._settings, text="Input upsampling number (from 0 to 4)", font="Arial 11").place(x=5, y=0)
        self.__text_upsampling = tkinter.Text(self._settings, width=5, height=1)
        self.__text_upsampling.place(x=275, y=3)

        self._button_confirm.place(x=150, y=33)

        self._set_saved_settings()

        self._settings.transient(root)
        self._settings.grab_set()
        self._settings.mainloop()

    def _set_saved_settings(self):
        if self.upsampling_number != None:
            self.__text_upsampling.insert(1.0, str(self.upsampling_number))

    def _save_settings(self):
        try:
            self.upsampling_number = int(self.__text_upsampling.get("1.0", tkinter.END))
            if self.upsampling_number < 0 or self.upsampling_number > 4:
                messagebox.showerror("Upsampling number error", "Argument \'Upsampling number\' is out of range")
                self.upsampling_number = None
            else:
                messagebox.showinfo("Settings save",
                                    "Settings have been saved successfully\nYou may close settings window or make changes")
        except:
            messagebox.showerror("Upsampling number error", "Incorrect upsampling number input")
            self.upsampling_number = None
