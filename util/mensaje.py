import customtkinter as ctk
from util.generic import Utilidades

class CustomMessageBox(ctk.CTkToplevel, Utilidades):
    def __init__(self, master, title, message, tipo):
        super().__init__(master)
        self.title(title)
        self.iconbitmap("./src/logo.ico")
        self.geometry("250x150")
        self.configure(fg_color='#2e2e2e')  # Fondo oscuro
        
        self.info = self.leer_imagen("./src/info2.png", (64, 64))
        self.error = self.leer_imagen("./src/error.png", (64, 64))
        
        self.centrar_ventana(self, 250, 150)
        
        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)
        self.focus_force()
        
        
        

        if tipo == "info":
                        
            self.label_message = ctk.CTkLabel(self, text=message, image=self.info, compound="left", fg_color='transparent', text_color="white")
            self.label_message.pack(pady=20)
            
        if tipo == "error":
                        
            self.label_message = ctk.CTkLabel(self, text=message, image=self.error, compound="left", fg_color='transparent', text_color="white")
            self.label_message.pack(pady=20)
            
        self.button_ok = ctk.CTkButton(self, text="OK", command=self.destroy, border_width=0, corner_radius=10)
        self.button_ok.pack(pady=10)
        
        
    
    def centrar_ventana(self, ventana,aplicacion_ancho, aplicacion_largo):
        
        pantall_ancho = ventana.winfo_screenwidth()
        pantall_largo = ventana.winfo_screenheight()
        x = int((pantall_ancho/2) - (aplicacion_ancho/2))
        y = int((pantall_largo/2) - (aplicacion_largo/2))
        return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
        
