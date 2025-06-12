import customtkinter as ctk
from views.auth.base_auth_visual import BaseAuthVisualView

class RegisterView(BaseAuthVisualView):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, titulo="Registrar Usuario", es_login=False, **kwargs)

    def crear_contenido_especifico(self):
        self.crear_titulo("Registrar Nuevo Usuario")

        # Campos de entrada
        self.entry_usuario = self.crear_campo(self.frame_contenido, "Usuario:")
        self.entry_password = self.crear_campo(self.frame_contenido, "Contraseña:", es_password=True)
        self.entry_confirmar = self.crear_campo(self.frame_contenido, "Confirmar Contraseña:", es_password=True)

        # Botón Registrar
        self.button_registrar = ctk.CTkButton(
            self.frame_contenido, text="   Siguiente   ", command=self.registrar_usuario
        )
        self.button_registrar.pack(fill=ctk.X, padx=20, pady=(15, 10))

        # Botón Volver
        self.button_volver = ctk.CTkButton(
            self.frame_contenido, text="Volver", command=self.controller["Mostrar_Ventanas"].mostrar_vista_login
        )
        self.button_volver.pack(fill=ctk.X, padx=20, pady=0)

    def registrar_usuario(self):
        nuevo_usuario = self.entry_usuario.get()
        nueva_contraseña = self.entry_password.get()
        confi_contraseña = self.entry_confirmar.get()

        if not nuevo_usuario or not nueva_contraseña or not confi_contraseña:
            self.mostrar_mensaje("Mensaje", "Error: campos vacíos", "error")
        else:
            # Aquí deberías tener tu lógica de verificación de usuario y registro
            if True:#hasattr(self.controller, "registro_controlador") and \
               #self.controller.registro_controlador.verificarUsuario(nuevo_usuario):
                self.mostrar_mensaje("Mensaje", "Error: el usuario ya existe", "error")
            else:
                if nueva_contraseña != confi_contraseña:
                    self.mostrar_mensaje("Mensaje", "Error: las contraseñas son diferentes", "error")
                else:
                    # Aquí puedes llamar a la función para mostrar la siguiente vista o guardar el usuario
                    if True:#hasattr(self.controller, "mostrar_vista_preguntas"):
                        self.mostrar_mensaje("Mensaje", "Registro exitoso (simulado)", "info")
                        #self.controller.mostrar_vista_preguntas(nuevo_usuario, "", nueva_contraseña)
                    else:
                        self.mostrar_mensaje("Mensaje", "Registro exitoso (simulado)", "info")

    def validarCampo(self, text):
        return text.isdecimal() and len(text) <= 8 or text == ""