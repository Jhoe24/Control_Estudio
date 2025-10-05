# archivo : views/dashboard/pages/admin_dashboard.py
import customtkinter as ctk
from views.dashboard.base_dashboard import BaseDashboardView
from config.settings import Settings

from views.dashboard.components.label_Bienvenida import LabelBienvenida
from views.dashboard.components.card import Card, CardDisplay

from views.dashboard.modules.Carga_notas import CargaNotasView
from views.dashboard.modules.Solicitud_doc import SolicitudDoc
from views.dashboard.modules.tables.Carga_notas.List_estudiantes_notas import ListadosEstudiantesNotas
from views.dashboard.modules.tables.Estudiantes.ListarEstudiantes import ListEstudiantesView

#from views.dashboard.modules.Sedes import ListSedesView

from views.dashboard.modules.configuracion import Config_user
from views.dashboard.modules.configuracion_sistema import Config_system

class EstudianteDashboardView(BaseDashboardView):
    
    def __init__(self, master, controller, username, user_role, **kwargs):
        super().__init__(master, controller, username, user_role, **kwargs)
        self.master = master
        self.controller = controller
        self.username = username
        self.user_role = user_role

        # Obtener datos completos del usuario/estudiante
        self.datos_estudiante = self.controller["Usuario"].obtener_datos_completos_usuario(self.username)
        self.inicio()
    
    def inicio(self):
        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        ruta = Settings().rutas_iconos.get("faces_icon")

        # --- Personalizar bienvenida y obtener datos para las tarjetas ---
        nombre_estudiante = self.datos_estudiante.get("nombres", "") if self.datos_estudiante else ""
        self.estudiante_id = self.datos_estudiante.get("estudiante_id") if self.datos_estudiante else None

        if self.estudiante_id:
            # Obtener datos de las tarjetas            
            datos_pnf_asignado = self.controller['PNF'].modelo.obtener_pnf_asignado(self.estudiante_id)

            promedio = datos_pnf_asignado.get("promedio_general", 0.0) if datos_pnf_asignado else 0.0
            # Obtener el nombre del trayecto directamente, ya que se guarda como texto
            nombre_trayecto = datos_pnf_asignado.get("trayecto_actual", "N/A") if datos_pnf_asignado else "N/A"
            
            # Obtener el ID del trayecto usando el nombre y el pnf_id
            pnf_id = datos_pnf_asignado.get("pnf_id") if datos_pnf_asignado else None
            trayecto_id = self.controller['PNF'].modelo.obtener_id_por_nombre_y_pnf("trayectos", nombre_trayecto, pnf_id) if pnf_id else None

            # Llamar al método corregido que ahora sabe cómo manejar el nombre del trayecto
            uc_inscritas = self.controller['Estudiantes'].modelo.contar_uc_inscritas_estudiante(trayecto_id) if trayecto_id else 0
        else:
            uc_inscritas, promedio, nombre_trayecto = 0, 0.0, "N/A"

        # Mostrar bienvenida usando el componente LabelBienvenida
        bienvenida = LabelBienvenida(self.cuerpo_principal)
        bienvenida.pack(fill="x", padx=10, pady=10)
        bienvenida.configurar(
            titulo=f"¡Bienvenido, {nombre_estudiante}!",
            mensaje="Aquí puedes consultar tus notas, ver tu progreso académico y mantenerte al día con tus estudios. ¡Sigue adelante!",
            icono_path=ruta,
            alineacion="center"
        )
            # Información de las tarjetas
        cards_info1 = [
            ("UCs Inscritas (Periodo Actual)", uc_inscritas, Settings().rutas_iconos.get("uc_icon")),
            ("Promedio General", f"{promedio:.2f}", Settings().rutas_iconos.get("notas_icon")),
            ("Trayecto Actual", nombre_trayecto, Settings().rutas_iconos.get("pnf_icon")),
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
                
        carga_notas = ListadosEstudiantesNotas(self.cuerpo_principal, self.controller, user=self.username)
        carga_notas.pack(fill="both", expand=True, padx=10, pady=10)

    def solicitud(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        solicitud = SolicitudDoc(self.cuerpo_principal, self.controller, rol = self.user_role, id = self.estudiante_id)
        solicitud.pack(fill="both", expand=True, padx=10, pady=10)
                

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
        
    