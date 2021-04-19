from tkinter import *
from tkinter import messagebox


class SettingsWindowHOG:
    def __init__(self, upsampling_number):
        self.upsampling_number = upsampling_number

    def open_dialog(self, root):
        self.settings = Toplevel()
        self.settings.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.settings.geometry("380x70")
        self.settings.title("CNN Settings")
        r = (self.settings.winfo_screenwidth() - self.settings.winfo_reqwidth()) / 2.5
        t = (self.settings.winfo_screenheight() - self.settings.winfo_reqheight()) / 2.5
        self.settings.wm_geometry("+%d+%d" % (r, t))
        self.settings.resizable(width=False, height=False)

        Label(self.settings, text="Input upsampling number (from 0 to 4)", font="Arial 11").place(x=5, y=0)
        self.text_upsampling = Text(self.settings, width=5, height=1)
        self.text_upsampling.place(x=275, y=3)

        self.button_confirm = Button(self.settings, text="Save settings", font="Arial 11", command=self.__save_settings)
        self.button_confirm.place(x=150, y=33)

        self.__set_saved_setting()

        self.settings.transient(root)
        self.settings.grab_set()
        self.settings.mainloop()

    def __on_closing(self):
        self.settings.grab_release()
        self.settings.quit()
        self.settings.destroy()

    def __set_saved_setting(self):
        if self.upsampling_number != None:
            self.text_upsampling.insert(1.0, str(self.upsampling_number))

    def __save_settings(self):
        try:
            self.upsampling_number = int(self.text_upsampling.get("1.0", END))
            if self.upsampling_number < 0 or self.upsampling_number > 4:
                messagebox.showerror("Upsampling number error", "Argument \'Upsampling number\' is out of range")
                self.upsampling_number = None
            else:
                messagebox.showinfo("Settings save",
                                    "Settings have been saved successfully\nYou may close settings window or make changes")
        except:
            messagebox.showerror("Upsampling number error", "Incorrect upsampling number input")
            self.upsampling_number = None
