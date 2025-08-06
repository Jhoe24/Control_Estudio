import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess
import platform

from views.dashboard.components.widget_utils import *

from config.app_config import AppConfig

class Config_system(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.master = master

        ctk.CTkLabel(
            self,
            text="Gestión de Datos de Docente",
            font=FUENTE_TITULO_FORMULARIO,
            text_color=COLOR_TEXTO_PRINCIPAL
        ).pack(pady=(10, 20), padx=20, anchor="w")

        # Frame de botones superiores
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(10, 20))

        self.btn_fecha_hora = ctk.CTkButton(
            self.button_frame, text="Configurar Fecha y Hora", width=180,
            command=self.abrir_configuracion_fecha_hora,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, # Asumiendo un color terciario
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT # Asumiendo un color terciario
        )
        self.btn_fecha_hora.pack(side="left", padx=10)

        # Frame donde se actualiza el contenido según el botón presionado
        self.contenido_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, pady=(10, 0))


    def limpiar_contenido_frame(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()

    def abrir_configuracion_fecha_hora(self):
        """
        Abre la configuración de fecha y hora del sistema operativo.
        Se adapta a Windows, macOS y Linux.
        """
        so = platform.system() #para detectar el S.O

        if so == "Windows":
            print("Abriendo configuración de fecha y hora en Windows...")
            try:
                subprocess.Popen(["control.exe","timedate.cpl"])
            except FileNotFoundError:
                messagebox.showerror("Error", "No se pudo encontrar 'timedate.cpl'.")

        elif so == "Darwin": # macOS
            print("Abriendo configuración de fecha y hora en macOS...")
            try:
                subprocess.Popen(["open", "/System/Library/PreferencePanes/DateAndTime.prefPane"])
            except FileNotFoundError:
                messagebox.showerror("Error", "No se pudo encontrar el panel de preferencias de macOS.")
        
        elif so == "Linux":
            print("Abriendo configuración de fecha y hora en Linux...")
            try:
                # Comandos comunes en distribuciones de Linux
                subprocess.Popen(["gnome-control-center", "datetime"])
            except FileNotFoundError:
                try:
                    subprocess.Popen(["kde-config-date"])
                except FileNotFoundError:
                    messagebox.showerror("Error", "No se encontró un comando de configuración de fecha y hora conocido en Linux.")
        
        else:
            messagebox.showinfo("Información", f"El sistema operativo '{so}' no está soportado para esta función.")




