# archivo : views/dashboard/pages/admin_dashboard.py
import customtkinter as ctk
from views.dashboard.base_dashboard import BaseDashboardView
from config.settings import Settings

from views.dashboard.components.label_Bienvenida import LabelBienvenida
from views.dashboard.components.card import Card, CardDisplay

from views.dashboard.modules.tables.Docentes.ListarDocentes import ListDocenteView

from views.dashboard.modules.PNF import FormularioPNFPensumView

from views.dashboard.modules.forms.UnidadCurricular import UnidadCurricular
from views.dashboard.modules.tables.PNF.ListarUC import ListarUC

from views.dashboard.modules.Carga_notas import CargaNotasView
#from views.dashboard.modules.Sedes import ListSedesView

from views.dashboard.modules.configuracion import Config_user
from views.dashboard.modules.configuracion_sistema import Config_system


class CoordinadorPNFDashboardView(BaseDashboardView):
    
    def __init__(self, master, controller, username, user_role, **kwargs):
        super().__init__(master, controller, username, user_role, **kwargs)
        self.master = master
        self.controller = controller
        self.username = username
        self.user_role = user_role
        self.datos_pnf = self.obtener_pnf()
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
            titulo="¡Bienvenido al Panel de Control del Coordinador P.N.F.!",
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
    
    def list_docente(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        list_docente = ListDocenteView(self.cuerpo_principal, self.controller,self.user_role, self.username)
        list_docente.pack(fill="both", expand=True, padx=10, pady=10)

    def pnf(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()

        pnf = FormularioPNFPensumView(self.cuerpo_principal, self.controller['PNF'])
        pnf.set_dato(self.datos_pnf)
        pnf.pack(fill="both", expand=True, padx=10, pady=10)
    
    def unid_Curr(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()

        unid_Curr = UnidadCurricular(self.cuerpo_principal, None, self.controller, user_name=self.username, rol_user=self.user_role)
        unid_Curr.pack(fill="both", expand=True, padx=10, pady=10)

    def listar_uc(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        listar_uc = ListarUC(self.cuerpo_principal, self.controller, user_role=self.user_role, username=self.username)
        listar_uc.pack(fill="both", expand=True, padx=10, pady=10)
    
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
        
    def obtener_pnf(self):
        persona_id = self.controller["Usuario"].obtener_persona_id(self.username)
        docente_id = self.controller["Docentes"].obtener_id_docente(persona_id)
        pnf_id = self.controller["Docentes"].obtener_pnf_id(docente_id)
        return self.controller["PNF"].obtener_pnf(pnf_id)
    
        