import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.base import VistaBase

class VistaInicioSesion(VistaBase):
    
    def __init__(self, master, controlador):
        # Llamamos al constructor de la clase base con es_login=True
        super().__init__(master, controlador, titulo="Iniciar Sesión...", es_login=True)
        
    def crear_contenido_especifico(self):
        # Crear título
        self.crear_titulo("Inicio de Sesión")
        
        # Crear campos de entrada
        self.LoginUsuario = self.crear_campo(self.frame_contenido, 'Usuario:')
        self.Loginpassword, self.verOcultar = self.crear_campo(self.frame_contenido, 'Contraseña:', es_password=True)
        
        # Crear enlace para recuperar contraseña
        self.btn_olvide = self.crear_boton_texto(
            self.frame_contenido,
            ' Has olvidado tu contraseña?',
            "Click Aqui",
            self.controlador.mostrar_vista_olvideClave
        )
        
        # Crear botón de iniciar sesión
        self.iniciar = self.crear_boton(
            self.frame_contenido,
            "Iniciar Sesión",
            self.login,
            pady=(20, 20)
        )
        
        # Crear enlace para registro
        self.registrarU = self.crear_boton_texto(
            self.frame_contenido,
            ' No tienes cuenta?',
            "Registrate Aqui",
            self.controlador.mostrar_vista_registro
        )
        
        # Crear enlace de ayuda
        self.btn_ayuda = self.crear_boton_texto(
            self.frame_contenido,
            ' Necesitas Ayuda?',
            "Click Aqui",
            self.abrir_pdf
        )
        
        self.LoginUsuario.bind("<Return>", lambda event: self.Loginpassword.focus())
        self.Loginpassword.bind("<Return>", lambda event: self.login())
        
    def login(self):
        # Obtener los datos de entrada
        nombre_usuario = self.LoginUsuario.get()
        contraseña = self.Loginpassword.get()
        
        if len(nombre_usuario) == 0 or len(contraseña) == 0:
            CustomMessageBox(self.master, "Mensaje", "   Error campos vacios  ", 'error')
        else:
            # Llamar al método del controlador
            resultado = self.controlador.login_controlador.login(nombre_usuario, contraseña)
            if resultado:
                #CustomMessageBox(self.master, "Mensaje", "   Datos Correctos  ", 'info')
                id_usuario = self.controlador.login_controlador.obtener_idUsuario(nombre_usuario)
                self.controlador.mostrar_vista_master(id_usuario)
            else:
                CustomMessageBox(self.master, "Mensaje", "   Usuario o contraseña incorrectos  ", 'error')
               
