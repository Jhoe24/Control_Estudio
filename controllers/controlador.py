# importacion de la libreria customtkinter para diseño 
import customtkinter as ctk

# importacion de los ficheros vistas(diseños) y los controladores
from views.login_view import VistaInicioSesion
from views.register_view import VistaRegistroUsuario
from views.registerPreguntas_view import VistaRegisterPreguntas
from views.forgotpassword_view import VistaOlvideClave
from views.newpassword_view import vistaCambioClave
from views.admin.master_view import VistaMaster


from controllers.loginController import ControladorInicioSesion
from controllers.registerController import ControladorRegistroUsuario
from controllers.forgotpassController import ControladorOlvideClave

from controllers.masterController import ControladorMaster

class ControladorPrincipal:
    def __init__(self):
        self.root = ctk.CTk() # instanciamos la clase de ctk para crear la ventana
        self.vista_actual = None # nos sirvira para saber que vista se esta mostrando

        # Instancias de controladores de cada vista
        self.login_controlador = ControladorInicioSesion()
        self.registro_controlador = ControladorRegistroUsuario()
        self.olvideclave_controlador = ControladorOlvideClave()
        
        self.master_controlador = ControladorMaster(self.root)

        # mostramos la vista de login
        self.mostrar_vista_login()

    def mostrar_vista_login(self):
        if self.vista_actual: # si hay alguna vista abierta, con el pack forget se cierra
            self.vista_actual.pack_forget()
        self.vista_actual = VistaInicioSesion(self.root, self) # instanciamos la vista del login
        self.vista_actual.pack() # mostramos la vista

    def mostrar_vista_registro(self):
        if self.vista_actual:
            self.vista_actual.pack_forget()
        self.vista_actual = VistaRegistroUsuario(self.root, self)
        self.vista_actual.pack()
    
    def mostrar_vista_preguntas(self, nuevo_usuario, nueva_cedula, nueva_contraseña):
        if self.vista_actual:
            self.vista_actual.pack_forget()
        self.vista_actual = VistaRegisterPreguntas(self.root, self, nuevo_usuario, nueva_cedula, nueva_contraseña)
        self.vista_actual.pack()
    
    def mostrar_vista_olvideClave(self):
        if self.vista_actual:
            self.vista_actual.pack_forget()
        self.vista_actual = VistaOlvideClave(self.root, self)
        self.vista_actual.pack()
        
    def mostrar_vista_cambioClave(self, usuario):
        if self.vista_actual:
            self.vista_actual.pack_forget()
        self.vista_actual = vistaCambioClave(self.root, self, usuario)
        self.vista_actual.pack()
    
    
    
    def mostrar_vista_master(self, usuario):
        if self.vista_actual:
            self.vista_actual.pack_forget()
        self.vista_actual = VistaMaster(self.root, self, usuario)
        self.vista_actual.pack()

    def run(self):
        self.root.mainloop() #ejecutamos la ventana para que se muestre
