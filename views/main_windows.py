import customtkinter as ctk

from views.auth.login_view import LoginView
from views.auth.register_view import RegisterView

from views.dashboard.pages.admin_dashboard import AdminDashboardView

from controllers.auth.auth_controller import AuthController
from services.usuario_services import UsuarioService

from controllers.dashboard.RegistroEstudiantes.RegistroEstudiante import EstudianteController
from controllers.dashboard.RegistroDocentes.RegistroDocentes import DocenteController
from controllers.dashboard.PNF.controller_pnf import ControllerPNF
from controllers.dashboard.Periodos_Academicos.Controller_ProAcad import PeriodoAcademicoController
from controllers.dashboard.Sedes.Controllers_sedes import ControladorSedes



from config.app_config import AppConfig


class MainWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.titulo = AppConfig().titulo_ventana  # Titulo de la ventana
        
        ancho_pantalla = self.winfo_screenwidth()  
        alto_pantalla = self.winfo_screenheight()
        
        tamano = AppConfig().evaluar_tamano_pantalla(ancho_pantalla, alto_pantalla)  # Evaluamos el tamaño de la pantalla
        self.tamano_ventana =  tamano
        #print(type(self.tamano_ventana))
        
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
            "PNF": ControllerPNF(),
            "Periodos": PeriodoAcademicoController(),
            "Sedes": ControladorSedes() ,
            }  # Aquí se inicializa el controlador del dashboard, que es el panel de control de la aplicación. 
        # El servicio de usuario se inyecta en el controlador de autenticación, cuya funcion es manejar la lógica de autenticación y autorización de usuarios. 

        # Mostramos la vista de login al iniciar la aplicación
        self.mostrar_vista_login()
        #self.mostrar_vista_dashboardd("Master", "admin")  # Por defecto mostramos el dashboard de admin, pero esto se puede cambiar dependiendo del rol del usuario que inicie sesión.
    
    def limpiar_vista_actual(self):
        if self.vista_actual:
            self.vista_actual.destroy()
            self.vista_actual = None
    
    def mostrar_vista_login(self):
        self.limpiar_vista_actual()
        self.title(self.titulo + "  -  " + "Inicio de Sesion ")  # Cambiamos el titulo de la ventana a Login
        self.vista_actual = LoginView(self, self.auth_controller)
        self.vista_actual.pack(fill="both", expand=True, padx=10, pady=10) # Aplicamos el padding aquí
    
        AppConfig().centrar_ventana(self, *self.tamano_ventana.split("x"))  # Centramos la ventana en la pantalla
   

    def mostrar_vista_registro(self):
        self.limpiar_vista_actual()
        self.title(self.titulo + "  -  " + "Registro de Usuario")
        self.vista_actual = RegisterView(self, self.auth_controller)
        self.vista_actual.pack(fill="both", expand=True, padx=10, pady=10) # Aplicamos el padding aquí
        
        
        # nuevo_tamano = str(self.winfo_screenmmwidth())+"x"+str(self.winfo_screenmmheight())
        # AppConfig().centrar_ventana(self, nuevo_tamano.split("x"))  

    def mostrar_vista_dashboardd(self, username, user_rol):
        # Limpiamos la vista actual antes de mostrar el dashboard
        self.limpiar_vista_actual()
        self.resizable(True, True)
    
        self.title(self.titulo + "  -  " + "Dashboard")
        
        # 1. Maximizar la ventana ANTES de crear la vista.
        self.state('zoomed') 
        # 2. Forzar la actualización para que el tamaño maximizado se aplique
        # y esté disponible para los widgets que se crearán.
        self.update_idletasks()
        self.after(50, lambda: self._create_dashboard_view(username, user_rol)) # Pequeño retraso para asegurar que 'zoomed' se aplique
        
        # 3. Traer la ventana al frente.
        self.lift()
        self.attributes("-topmost", True) # Esto asegura que la ventana esté en primer plano
        self.after(100, lambda: self.attributes("-topmost", False)) # Esto quita el atributo de estar siempre en primer plano después de 100ms
        self.focus_force()  # Aseguramos que la ventana esté en primer plano

    def _create_dashboard_view(self, username, user_rol):
        """Método auxiliar para crear la vista del dashboard después de un pequeño retraso."""
        # Dependiendo del rol del usuario, mostramos la vista correspondiente
        if user_rol == "admin":
            self.vista_actual = AdminDashboardView(self, self.dashboard_controller, username, user_rol)


    def run(self):
        self.mainloop()
    
    