import customtkinter as ctk

from views.auth.login_view import LoginView
from views.auth.register_view import RegisterView

from views.dashboard.pages.admin_dashboard import AdminDashboardView

from controllers.auth.auth_controller import AuthController
from services.usuario_services import UsuarioService

from controllers.dashboard.RegistroEstudiantes.RegistroEstudiante import EstudianteController
from controllers.dashboard.RegistroDocentes.RegistroDocentes import DocenteController
from controllers.dashboard.PNF.controller_pnf import ControllerPNF



from config.app_config import AppConfig


class MainWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.titulo = AppConfig().titulo_ventana  # Titulo de la ventana
        
        ancho_pantalla = self.winfo_screenwidth()  
        alto_pantalla = self.winfo_screenheight()
        
        tamano = AppConfig().evaluar_tamano_pantalla(ancho_pantalla, alto_pantalla)  # Evaluamos el tamaño de la pantalla
        self.tamano_ventana =  tamano
        
        
        self.icono = AppConfig().icono
        self.tema = AppConfig().tema
        
        self.title(self.titulo)
        self.geometry(self.tamano_ventana)
        self.resizable(False, False)  # No permitimos que la ventana sea redimensionable al inicio
        self.iconbitmap(self.icono)  
        
        # Configuración del tema y colores
        ctk.set_appearance_mode(self.tema)
        
        AppConfig().centrar_ventana(self, *self.tamano_ventana.split("x"))  # Centramos la ventana en la pantalla
        
        self.vista_actual = None # Declaramos una variable para la vista actual
        
        self.auth_controller = {
            "Mostrar_Ventanas": self,
            "Autenticacion": (AuthController(UsuarioService), self)
            }  # Aquí se inicializa el controlador de autenticación, osea lo del login, registro, etc.
        self.dashboard_controller = {
            "Estudiantes": EstudianteController(),
            "Docentes":  DocenteController(),
            "PNF": ControllerPNF()
            }  # Aquí se inicializa el controlador del dashboard, que es el panel de control de la aplicación. 
        # El servicio de usuario se inyecta en el controlador de autenticación, cuya funcion es manejar la lógica de autenticación y autorización de usuarios. 
        
        # Mostramos la vista de login al iniciar la aplicación
        #self.mostrar_vista_login()
        self.mostrar_vista_dashboardd("Master", "admin")  # Por defecto mostramos el dashboard de admin, pero esto se puede cambiar dependiendo del rol del usuario que inicie sesión.
    
    def limpiar_vista_actual(self):
        if self.vista_actual:
            self.vista_actual.destroy()
            self.vista_actual = None
    
    def mostrar_vista_login(self):
        self.limpiar_vista_actual()
        self.title(self.titulo + "  -  " + "Inicio de Sesion ")  # Cambiamos el titulo de la ventana a Login
        self.vista_actual = LoginView(self, self.auth_controller)  # Pasamos el controlador de autenticación a la vista de login
        self.vista_actual.pack(fill="both", expand=True)   

    def mostrar_vista_registro(self):
        self.limpiar_vista_actual()
        self.title(self.titulo + "  -  " + "Registro de Usuario")
        self.vista_actual = RegisterView(self, self.auth_controller)
        self.vista_actual.pack(fill="both", expand=True)    

    def mostrar_vista_dashboardd(self, username, user_rol):
        # Limpiamos la vista actual antes de mostrar el dashboard
        self.limpiar_vista_actual()
        self.resizable(True, True)
        
        ancho_pantalla = self.winfo_screenwidth()  
        alto_pantalla = self.winfo_screenheight()
        tamano_ventana = (str(ancho_pantalla)+"x"+str(alto_pantalla))
        # Cambiamos el titulo de la ventana a Dashboard

        self.title(self.titulo + "  -  " + "Dashboard")
        
        # self.geometry(str(ancho_pantalla)+"x"+str(alto_pantalla))
        # AppConfig().centrar_ventana(self, *tamano_ventana.split("x"))
        # self.update_idletasks()
        
        self.state('zoomed') 
        # Dependiendo del rol del usuario, mostramos la vista correspondiente
        if user_rol == "admin":
            from views.dashboard.pages.admin_dashboard import AdminDashboardView
            self.vista_actual = AdminDashboardView(self, self.dashboard_controller, username, user_rol)
            ancho = self.winfo_width()
            alto = self.winfo_height()
            
        
        self.lift()
        self.attributes("-topmost", True) # Esto asegura que la ventana esté en primer plano
        self.after(100, lambda: self.attributes("-topmost", False)) # Esto quita el atributo de estar siempre en primer plano después de 100ms
        self.focus_force()  # Aseguramos que la ventana esté en primer plano
        

    def run(self):
        self.mainloop()
    
    