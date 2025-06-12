import customtkinter as ctk
from PIL import Image

class UtilImagen:
    
    def leer_imagen(self, vista, ruta, tamano=None):
        try:
            if tamano is None:
                # Asegúrate de que el widget ya esté renderizado para obtener el tamaño correcto
                vista.update_idletasks()
                ancho = vista.winfo_width()
                alto = vista.winfo_height()
                # Si el tamaño aún es 1 (no renderizado), usa un valor por defecto
                if ancho <= 1 or alto <= 1:
                    ancho, alto = 100, 100
                tamano = (ancho, alto)
            return ctk.CTkImage(light_image=Image.open(ruta), dark_image=Image.open(ruta), size=tamano)
        except Exception as e:
            print(f"Error al leer la imagen {ruta}: {e}")
            return None