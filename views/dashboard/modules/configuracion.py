import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox

from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from views.dashboard.components.widget_utils import *

from config.app_config import AppConfig

class Config_user(ctk.CTkFrame):
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

        self.btn_contrasena = ctk.CTkButton(
            self.button_frame, text="Cambio de Contraseña", width=150,
            command=self.mostrar_cambiar_contrasena,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        self.btn_contrasena.pack(side="left", padx=20)

        self.btn_datos = ctk.CTkButton(
            self.button_frame, text="Cambio de Datos Personales", width=150,
            command=self.mostrar_cambiar_datos_personales,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT
        )
        self.btn_datos.pack(side="left", padx=20)

        self.btn_desbloqueo = ctk.CTkButton(
            self.button_frame, text="Desbloqueo de Usuarios", width=150,
            command=self.mostrar_desbloqueo_usuarios,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        self.btn_desbloqueo.pack(side="left", padx=20)

        # Frame donde se actualiza el contenido según el botón presionado
        self.contenido_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, pady=(10, 0))

        

    def limpiar_contenido_frame(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()

    def mostrar_cambiar_contrasena(self):
        self.limpiar_contenido_frame()

        # Frame interno para campos (para alinearlos arriba)
        form_frame = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        form_frame.pack(anchor="n", pady=20, fill="both", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # Campos de contraseña actual y nueva en form_frame
        self._crear_fila_widgets([
            ("Contraseña actual:", crear_entry, {"width": 300}, 1, form_frame, 'password_hash_entry'),
            ("Contraseña nueva:", crear_entry, {"width": 300}, 1, form_frame, 'cambiar_password_entry')
        ])

        # Botón actualizar debajo de form_frame
        btn_actualizar = ctk.CTkButton(
            self.contenido_frame, text="Actualizar Contraseña",
            command=lambda: messagebox.showinfo("Info", "Contraseña actualizada correctamente"),
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        btn_actualizar.pack(pady=10)

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
        

    def mostrar_cambiar_datos_personales(self):
        self.limpiar_contenido_frame()

        form_frame = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        form_frame.pack(anchor="n", pady=20, fill="both", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        self._crear_fila_widgets([
            ("Usuario:", crear_entry, {"width": 300}, 1, form_frame, 'nombre_usuario_entry'),
            ("Nombres:", crear_entry, {"width": 300}, 1, form_frame, 'nombres_entry'),
            ("Apellidos:", crear_entry, {"width": 300}, 1, form_frame, 'apellidos_entry'),
            ("Correo Electrónico:", crear_entry, {"width": 300}, 1, form_frame, 'correo_electronico_entry')
        ])

        btn_actualizar = ctk.CTkButton(
            self.contenido_frame, text="Actualizar Datos Personales",
            command=lambda: messagebox.showinfo("Info", "Datos personales actualizados correctamente"),
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT
        )
        btn_actualizar.pack(pady=10)
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets



    def mostrar_desbloqueo_usuarios(self):
        self.limpiar_contenido_frame()

        #Apartado para mostrar a los usuarios bloqueados y desbloquearlos

        btn_desbloquear = ctk.CTkButton(
            self.contenido_frame, text="Desbloquear Usuario",
            command=lambda: messagebox.showinfo("Info", "Usuario desbloqueado correctamente"),
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        btn_desbloquear.pack(pady=10)


