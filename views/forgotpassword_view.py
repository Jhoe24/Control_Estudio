import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.base import VistaBase

class VistaOlvideClave(VistaBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, titulo="Recuperar Contraseña")
        
    def crear_contenido_especifico(self):
        # Crear título
        self.crear_titulo("Recuperar Contraseña")
        
        # Crear campos específicos para esta vista
        self.LoginUsuario = self.crear_campo(self.frame_contenido, 'Usuario:')
        
        # Crear una etiqueta explicativa
        etiqueta_info = ctk.CTkLabel(
            self.frame_contenido, 
            text="Ingrese su nombre de usuario para recuperar su contraseña.\nSe le solicitarán sus preguntas de seguridad.",
            font=('Times', 14),
            text_color="#fff"
        )
        etiqueta_info.pack(fill=ctk.X, padx=20, pady=10)
        
        # Crear botones
        self.recuperar = self.crear_boton(
            self.frame_contenido,
            "Verificar Usuario",
            self.recuperar_clave,
            pady=(20, 10)
        )
        
        self.volver = self.crear_boton(
            self.frame_contenido,
            "Volver",
            self.controlador.mostrar_vista_login,
            pady=10
        )
    
    def recuperar_clave(self):
        # Obtener el nombre de usuario
        nombre_usuario = self.LoginUsuario.get()
        
        if len(nombre_usuario) == 0:
            CustomMessageBox(self.master, "Mensaje", "   Error campo vacío  ", 'error')
        else:
            # Verificar si el usuario existe
            if self.controlador.olvideclave_controlador.verificarUsuario(nombre_usuario):
                # Si existe, mostrar vista para cambiar contraseña
                self.controlador.mostrar_vista_cambioClave(nombre_usuario)
            else:
                # Si no existe, mostrar mensaje de error
                CustomMessageBox(self.master, "Mensaje", "   El usuario no existe  ", 'error')      
        
    