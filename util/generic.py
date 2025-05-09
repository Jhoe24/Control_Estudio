import customtkinter as ctk
from PIL import Image
import webbrowser

class Utilidades:
    
    def leer_imagen(self, ruta, tamano):
        return ctk.CTkImage(light_image=Image.open(ruta), dark_image=Image.open(ruta), size=(tamano))
    
    def centrar_ventana(self, ventana,aplicacion_ancho, aplicacion_largo):    
        pantall_ancho = ventana.winfo_screenwidth()
        pantall_largo = ventana.winfo_screenheight()
        x = int((pantall_ancho/2) - (aplicacion_ancho/2))
        y = int((pantall_largo/2) - (aplicacion_largo/2))
        return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

    def alternar_visibilidad_clave(self, entryCampo, btn_verOcultar, icon, icon2):    
        if entryCampo.cget('show') == '*':
            entryCampo.configure(show='')
            btn_verOcultar.configure(image=icon)
        else:
            entryCampo.configure(show='*')
            btn_verOcultar.configure(image=icon2)

    def mostrarclave(self, campo, entryCampo, btn_verOcultar, icon, icon2):
        if campo == 'clave':
            self.alternar_visibilidad_clave(entryCampo, btn_verOcultar, icon, icon2)
        if campo == 'confirmar':
            self.alternar_visibilidad_clave(entryCampo, btn_verOcultar, icon, icon2)

    def abrir_pdf(self):
        # Construir la ruta completa del archivo PDF dentro de la carpeta principal 'app2'
        ruta_pdf = "manual.pdf"

        # Abrir el archivo PDF con el navegador predeterminado
        webbrowser.open_new(ruta_pdf)





    