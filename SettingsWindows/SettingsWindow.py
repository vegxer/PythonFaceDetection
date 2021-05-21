from abc import abstractmethod
import tkinter


class SettingsWindow():

    @abstractmethod
    def _on_closing(self):
        pass

    @abstractmethod
    def _save_settings(self):
        pass

    @abstractmethod
    def _set_saved_settings(self):
        pass

    @abstractmethod
    def open_dialog(self, root):
        pass

    def _init_window(self):
        self._settings = tkinter.Toplevel()
        self._button_confirm = tkinter.Button(self._settings, text="Save settings", font="Arial 11",
                                              command=self._save_settings)
