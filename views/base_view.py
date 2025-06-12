import customtkinter as ctk
from tkinter import messagebox as CTkMessageBox
from PIL import Image

class BaseView(ctk.CTkFrame):
    
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.pack(fill="both", expand=True)
         
    
    
    def mostrar_mensaje(self, titulo, mensaje, tipo_mensaje="info"):
        if tipo_mensaje == "info":
            CTkMessageBox.showinfo(title=titulo, message=mensaje)
        elif tipo_mensaje == "warning":
            CTkMessageBox.showwarning(title=titulo, message=mensaje)
        elif tipo_mensaje == "error":
            CTkMessageBox.showerror(title=titulo, message=mensaje)
        else:
            raise ValueError("Tipo de mensaje no válido")
    
    def limpiar_vista_widget(self):
        # Funcion que nos servira para limpiar los widgets de la vista actual
        # Esto es util cuando queremos cambiar de vista y no queremos que se acumulen widgets
        for widget in self.winfo_children():
            widget.destroy()
    
    def insertar_controlador(self, controller):
        # Funcion que nos servira para insertar un controlador en la vista actual
        # Esto es util cuando queremos cambiar de controlador y no queremos que se acumulen controladores
        self.controller = controller
    
    def actualizar_vista(self):
        # Funcion que nos servira para actualizar la vista actual
        # Esto es util cuando queremos actualizar la vista sin cambiar de vista
        self.limpiar_vista_widget()
        self.create_widgets()
    
    def create_widgets(self):
        # Esta funcion debe ser implementada en las vistas hijas
        # Aqui se deben crear los widgets de la vista actual
        raise NotImplementedError("La funcion create_widgets debe ser implementada en las vistas hijas")

    def leer_imagen(self, ruta, tamano=None):
        try:
            if tamano is None:
                # Asegúrate de que el widget ya esté renderizado para obtener el tamaño correcto
                self.update_idletasks()
                ancho = self.winfo_width()
                alto = self.winfo_height()
                # Si el tamaño aún es 1 (no renderizado), usa un valor por defecto
                if ancho <= 1 or alto <= 1:
                    ancho, alto = 100, 100
                tamano = (ancho, alto)
            return ctk.CTkImage(light_image=Image.open(ruta), dark_image=Image.open(ruta), size=tamano)
        except Exception as e:
            print(f"Error al leer la imagen {ruta}: {e}")
            return None