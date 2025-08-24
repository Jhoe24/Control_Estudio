# archivo : views/dashboard/pages/admin_dashboard.py
import customtkinter as ctk
from views.dashboard.base_dashboard import BaseDashboardView
from config.settings import Settings

from views.dashboard.components.label_Bienvenida import LabelBienvenida
from views.dashboard.components.card import Card, CardDisplay

from views.dashboard.modules.Carga_notas import CargaNotasView

from views.dashboard.modules.configuracion import Config_user
from views.dashboard.modules.configuracion_sistema import Config_system

class DocenteDashboardView(BaseDashboardView):
    
    def __init__(self, master, controller, username, user_role, **kwargs):
        super().__init__(master, controller, username, user_role, **kwargs)
        self.master = master
        self.controller = controller
        self.username = username
        self.user_role = user_role
        self.inicio()
    
    def inicio(self):
        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
            
        ruta = Settings().rutas_iconos.get("faces_icon")

        # Mostrar bienvenida usando el componente LabelBienvenida
        bienvenida = LabelBienvenida(self.cuerpo_principal)
        bienvenida.pack(fill="x", padx=10, pady=10)
        bienvenida.configurar(
            titulo="¡Bienvenido al Panel de Control del Docente!",
            mensaje="Hay mucho por hacer 🚀\n\nLos datos indican que nuestra universidad está en constante crecimiento.\n¡Gracias por tu gestión!",
            icono_path=ruta,
            alineacion="center"
        )
            # Información de las tarjetas
        cards_info1 = [
            ("Estudiantes Activos", 3241, Settings().rutas_iconos.get("estudiantes_icon", "resources/icons/estudiantes.png")),
            ("Docentes Activos", 1048, Settings().rutas_iconos.get("docentes_icon", "resources/icons/docentes.png")),
            ("Cursos Disponibles", 45, None),
        ]
        # Crear una CardDisplay
        card_display_frame = ctk.CTkFrame(self.cuerpo_principal, fg_color="transparent")
        card_display_frame.pack(side=ctk.TOP, fill="x", expand=True, pady=20, padx=20)
        
        card_display_frame.grid_columnconfigure(0, weight=1) # Centrar el CardDisplay

        card_display = CardDisplay(card_display_frame, cards_info1)
        card_display.grid(row=0, column=0, sticky="nsew")

    def carga_notas(self): 
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        carga_notas = CargaNotasView(self.cuerpo_principal,self.controller,user=self.username, rol=self.user_role)
        carga_notas.pack(fill="both", expand=True, padx=10, pady=10)
    
    def configuracion_usuarios(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        configuracion = Config_user(self.cuerpo_principal, self.controller,username=self.username,user_rol=self.user_role)
        configuracion.pack(fill="both", expand=True, padx=10, pady=10)

    def configuracion_sistema(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()

        configuracion = Config_system(self.cuerpo_principal)
        configuracion.pack(fill="both", expand=True, padx=10, pady=10)
        
    