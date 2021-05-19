import tkinter
from tkinter import messagebox


class SettingsWindowHOG:
    def __init__(self, upsampling_number=None):
        self.upsampling_number = upsampling_number

    def open_dialog(self, root):
        self.__settings = tkinter.Toplevel()
        self.__settings.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__settings.geometry("380x70")
        self.__settings.title("HOG Settings")
        r = (self.__settings.winfo_screenwidth() - self.__settings.winfo_reqwidth()) / 2.5
        t = (self.__settings.winfo_screenheight() - self.__settings.winfo_reqheight()) / 2.5
        self.__settings.wm_geometry("+%d+%d" % (r, t))
        self.__settings.resizable(width=False, height=False)

        tkinter.Label(self.__settings, text="Input upsampling number (from 0 to 4)", font="Arial 11").place(x=5, y=0)
        self.__text_upsampling = tkinter.Text(self.__settings, width=5, height=1)
        self.__text_upsampling.place(x=275, y=3)

        self.__button_confirm = tkinter.Button(self.__settings, text="Save settings", font="Arial 11",
                                               command=self.__save_settings)
        self.__button_confirm.place(x=150, y=33)

        self.__set_saved_setting()

        self.__settings.transient(root)
        self.__settings.grab_set()
        self.__settings.mainloop()

    def __on_closing(self):
        self.__settings.grab_release()
        self.__settings.quit()
        self.__settings.destroy()

    def __set_saved_setting(self):
        if self.upsampling_number != None:
            self.__text_upsampling.insert(1.0, str(self.upsampling_number))

    def __save_settings(self):
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
