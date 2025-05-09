import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.base import VistaBase

class VistaRegistroUsuario(VistaBase):
    def __init__(self, master, controlador):
        # Llamamos al constructor de la clase base
        super().__init__(master, controlador, titulo="Registrar Usuario", es_login=False)
        
    def crear_contenido_especifico(self):
        # Crear título
        self.crear_titulo("Registrar Nuevo Usuario")
        
        # Crear campos de entrada
        self.LoginUsuario = self.crear_campo(self.frame_contenido, 'Usuario:')
        self.Loginpassword, self.verOcultar = self.crear_campo(self.frame_contenido, 'Contraseña:', es_password=True)
        self.Confipassword, self.verOcultar2 = self.crear_campo(self.frame_contenido, 'Confirmar Contraseña:', es_password=True)
        
        # Crear botones
        self.registrar = self.crear_boton(self.frame_contenido, "   Siguiente   ", self.registrar_usuario, padx=20, pady=(15, 10)) # Para evitar que se expanda horizontalmente
        
        self.volver = self.crear_boton(self.frame_contenido, "Volver", self.controlador.mostrar_vista_login, padx=20, pady=0)# Para evitar que se expanda horizontalmente
        
        # Configurar el segundo botón de ver/ocultar contraseña
        self.verOcultar2.configure(command=lambda: self.mostrarclave('confirmar', self.Confipassword, self.verOcultar2, self.icon, self.icon2))

    def registrar_usuario(self):
        nuevo_usuario = self.LoginUsuario.get()
        nueva_cedula = str(29634288)
        nueva_contraseña = self.Loginpassword.get()
        confi_contraseña = self.Confipassword.get()
        
        if len(nuevo_usuario) == 0 or len(nueva_cedula) == 0 or len(nueva_contraseña) == 0 or len(confi_contraseña) == 0:
            CustomMessageBox(self.master, "Mensaje", "   Error campos vacios  ", 'error')
        else:
            if self.controlador.registro_controlador.verificarUsuario(nuevo_usuario):
                CustomMessageBox(self.master, "Mensaje", "   Error el usuario ya existe  ", 'error')
            else:
                if nueva_contraseña != confi_contraseña:
                    CustomMessageBox(self.master, "Mensaje", "   Error las contraseñas son diferentes   ", 'error')
                else:
                    self.controlador.mostrar_vista_preguntas(nuevo_usuario, nueva_cedula, nueva_contraseña)
    
    def validarCampo(self, text):
        return text.isdecimal() and len(text) <= 8 or text == ""