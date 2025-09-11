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
        
        # Obtener datos del docente para personalizar el dashboard
        self.datos_docente = self.controller["Usuario"].obtener_datos_completos_usuario(self.username)

        self.inicio()
    
    def inicio(self):
        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
            
        ruta = Settings().rutas_iconos.get("faces_icon")

        # --- Personalizar bienvenida y obtener datos para las tarjetas ---
        nombre_docente = self.datos_docente.get("nombres", "") if self.datos_docente else ""
        docente_id = self.datos_docente.get("docente_id") if self.datos_docente else None

        if docente_id:
            # NOTA: Estos métodos deben ser creados en sus respectivos modelos
            uc_asignadas = self.controller['Docentes'].modelo_docente.contar_uc_asignadas_a_docente(docente_id)
            estudiantes_a_cargo = self.controller['Docentes'].modelo_docente.contar_estudiantes_a_cargo_docente(docente_id)
        else:
            uc_asignadas, estudiantes_a_cargo = 0, 0

        # Mostrar bienvenida usando el componente LabelBienvenida
        bienvenida = LabelBienvenida(self.cuerpo_principal)
        bienvenida.pack(fill="x", padx=10, pady=10)
        bienvenida.configurar(
            titulo=f"¡Bienvenido, Prof. {nombre_docente}!",
            mensaje="Desde aquí puedes gestionar tus unidades curriculares y cargar las notas de tus estudiantes. ¡Tu labor es esencial para su formación!",
            icono_path=ruta,
            alineacion="center"
        )
            # Información de las tarjetas
        cards_info1 = [
            ("UC Asignadas (Periodo Actual)", uc_asignadas, Settings().rutas_iconos.get("uc_icon")),
            ("Estudiantes a Cargo", estudiantes_a_cargo, Settings().rutas_iconos.get("estudiantes_icon")),
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
        
    