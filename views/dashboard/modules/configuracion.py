import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox

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
            self.button_frame, text="Cambio de Contraseña", width=180,
            command=self.mostrar_cambiar_contrasena,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        self.btn_contrasena.pack(side="left", padx=10)

        self.btn_datos = ctk.CTkButton(
            self.button_frame, text="Cambio de Datos Personales", width=180,
            command=self.mostrar_cambiar_datos_personales,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT
        )
        self.btn_datos.pack(side="left", padx=10)

        self.btn_desbloqueo = ctk.CTkButton(
            self.button_frame, text="Desbloqueo de Usuarios", width=180,
            command=self.mostrar_desbloqueo_usuarios,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        self.btn_desbloqueo.pack(side="left", padx=10)

        # Frame donde se actualiza el contenido según el botón presionado
        self.contenido_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido_frame.pack(fill="both", expand=True, pady=(10, 0))

    def limpiar_contenido_frame(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()

    def mostrar_cambiar_contrasena(self):
        self.limpiar_contenido_frame()

        form_frame = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        form_frame.pack(pady=30)

        # Contraseña actual
        label_actual = ctk.CTkLabel(form_frame, text="Contraseña actual:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
        label_actual.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.password_actual_entry = ctk.CTkEntry(form_frame, width=300, show="*", fg_color=COLOR_FONDO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL)
        self.password_actual_entry.grid(row=0, column=1, padx=10, pady=10)

        # Contraseña nueva
        label_nueva = ctk.CTkLabel(form_frame, text="Contraseña nueva:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
        label_nueva.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.cambiar_password_entry = ctk.CTkEntry(form_frame, width=300, show="*", fg_color=COLOR_FONDO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL)
        self.cambiar_password_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_actualizar = ctk.CTkButton(
            self.contenido_frame, text="Actualizar Contraseña",
            command=self.actualizar_contrasena,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        btn_actualizar.pack(pady=20)

    def mostrar_cambiar_datos_personales(self):
        self.limpiar_contenido_frame()

        form_frame = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        form_frame.pack(pady=30)

        campos = [
            ("Usuario:", False),
            ("Nombres:", False),
            ("Apellidos:", False),
            ("Correo Electrónico:", False),
        ]

        self.entries = {}

        for idx, (label_text, es_password) in enumerate(campos):
            label = ctk.CTkLabel(form_frame, text=label_text, font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            label.grid(row=idx, column=0, sticky="w", padx=10, pady=10)

            entry = ctk.CTkEntry(form_frame, width=300, show="*" if es_password else "", fg_color=COLOR_FONDO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL)
            entry.grid(row=idx, column=1, padx=10, pady=10)
            self.entries[label_text] = entry

        btn_actualizar = ctk.CTkButton(
            self.contenido_frame, text="Actualizar Datos Personales",
            command=self.actualizar_datos_personales,
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT
        )
        btn_actualizar.pack(pady=20)

    def mostrar_desbloqueo_usuarios(self):
        self.limpiar_contenido_frame()

        label = ctk.CTkLabel(
            self.contenido_frame, text="Aquí se mostrarán los usuarios bloqueados para desbloquear.",
            font=FUENTE_LABEL_CAMPO,
            text_color=COLOR_TEXTO_PRINCIPAL
        )
        label.pack(pady=20)

        btn_desbloquear = ctk.CTkButton(
            self.contenido_frame, text="Desbloquear Usuario",
            command=lambda: messagebox.showinfo("Éxito", "Usuario desbloqueado correctamente"),
            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        btn_desbloquear.pack(pady=10)
#======================================================================================================================================================================

    def actualizar_contrasena(self):
        contrasena_actual = self.password_actual_entry.get()
        contrasena_nueva = self.cambiar_password_entry.get()

        if not contrasena_actual or not contrasena_nueva:
            messagebox.showwarning("Advertencia", "Debes ingresar ambas contraseñas.")
            return


        # Guardar en la base de datos
        print("Contraseña actual:", contrasena_actual)
        print("Contraseña nueva:", contrasena_nueva)

        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente")

    def actualizar_datos_personales(self):
        usuario = self.entries["Usuario:"].get()
        nombres = self.entries["Nombres:"].get()
        apellidos = self.entries["Apellidos:"].get()
        correo = self.entries["Correo Electrónico:"].get()

        campos_a_actualizar = {}
        if usuario:
            campos_a_actualizar["usuario"] = usuario
        if nombres:
            campos_a_actualizar["nombres"] = nombres
        if apellidos:
            campos_a_actualizar["apellidos"] = apellidos
        if correo:
            campos_a_actualizar["correo"] = correo

        if not campos_a_actualizar:
            messagebox.showwarning("Advertencia", "Debes completar al menos un campo para actualizar.")
            return

        # Para pasarle al controlador el diccionario
        print("Campos a actualizar: ", campos_a_actualizar)

        messagebox.showinfo("Éxito", "Datos personales de Usuario actualizados correctamente.")


