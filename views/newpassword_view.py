import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.base import VistaBase

class vistaCambioClave(VistaBase):
    def __init__(self, master, controlador, usuario):
        super().__init__(master, controlador, titulo="Cambiar clave")
        self.usuario = usuario

    def crear_contenido_especifico(self):
        # Título de la vista
        self.crear_titulo("Cambio de clave")

        # Campo de nueva contraseña
        self.Loginpassword, self.verOcultar = self.crear_campo(
            self.frame_contenido,
            'Contraseña:',
            es_password=True
        )
        # Configurar botón mostrar/ocultar específico
        self.verOcultar.configure(
            command=lambda: self.mostrarclave(
                'clave', self.Loginpassword, self.verOcultar, self.icon, self.icon2
            )
        )

        # Campo de confirmación de contraseña
        self.Confipassword, self.verOcultar2 = self.crear_campo(
            self.frame_contenido,
            'Confirmar Contraseña:',
            es_password=True
        )
        self.verOcultar2.configure(
            command=lambda: self.mostrarclave(
                'confirmar', self.Confipassword, self.verOcultar2, self.icon, self.icon2
            )
        )

        # Botón para cambiar clave
        self.registrar = self.crear_boton(
            self.frame_contenido,
            "Cambiar clave",
            self.cambiarClave
        )

        # Botón para volver a la vista anterior
        self.volver = self.crear_boton(
            self.frame_contenido,
            "Volver",
            self.controlador.mostrar_vista_olvideClave
        )

    def cambiarClave(self):
        clave = self.Loginpassword.get()
        confi_clave = self.Confipassword.get()

        if not clave or not confi_clave:
            CustomMessageBox(self.master, "Mensaje", "   Campos vacíos  ", 'error')
        elif clave != confi_clave:
            CustomMessageBox(self.master, "Mensaje", "   Contraseñas no coinciden  ", 'error')
        else:
            # Actualizar la contraseña en el controlador
            self.controlador.olvideclave_controlador.cambioClave(self.usuario, clave)
            CustomMessageBox(self.master, "Mensaje", "   Cambio exitoso  ", 'info')
            self.controlador.mostrar_vista_login()

            
