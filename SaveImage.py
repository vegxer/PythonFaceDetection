import cv2
import pathlib
from tkinter import filedialog, NONE, messagebox


# статический класс для сохранения изображения
class SaveImage:
    # сохраняет изображение по указанному пути
    @staticmethod
    def save_as(image_name, img, face_found):
        if SaveImage.__image_correct(img, face_found):
            file_name = filedialog.asksaveasfilename()
            if file_name:
                cv2.imwrite(file_name + pathlib.Path(image_name).suffix, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # сохраняет изображение по тому пути, по которому оно было открыто
    @staticmethod
    def save(image_name, img, face_found):
        if SaveImage.__image_correct(img, face_found):
            cv2.imwrite(image_name, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # проверка правильности входных параметров
    @staticmethod
    def __image_correct(image, face_found):
        if image != NONE:
            if face_found:
                return True
            else:
                messagebox.showwarning("Save error", "Image hasn't been changed")
        else:
            messagebox.showwarning("Undefined image", "Image hasn't been loaded")
        return False
