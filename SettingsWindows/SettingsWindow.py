from abc import abstractmethod
import tkinter


# класс, от которого наследуются все классы, обеспечивающие найстроки и их интерфейс
class SettingsWindow:
    # при закрытии окна, уничтожить всё
    def _on_closing(self):
        self._settings.grab_release()
        self._settings.quit()
        self._settings.destroy()

    @abstractmethod
    def _save_settings(self):
        pass

    @abstractmethod
    def _set_saved_settings(self):
        pass

    @abstractmethod
    def open_dialog(self, root):
        pass

    # инициализация окна (_settings) с кнопкой "Save settings"
    def _init_window(self):
        self._settings = tkinter.Toplevel()
        self._button_confirm = tkinter.Button(self._settings, text="Save settings", font="Arial 11",
                                              command=self._save_settings)
