# archivo : views/dashboard/pages/admin_dashboard.py
import customtkinter as ctk
from views.dashboard.base_dashboard import BaseDashboardView
from config.settings import Settings

from views.dashboard.components.label_Bienvenida import LabelBienvenida
from views.dashboard.components.card import Card, CardDisplay

from views.dashboard.modules.RegistrarEstudiantes import FormularioEstudianteView
from views.dashboard.modules.tables.Estudiantes.ListarEstudiantes import ListEstudiantesView


from views.dashboard.modules.RegistrarDocentes import FormularioDocenteView
from views.dashboard.modules.tables.Docentes.ListarDocentes import ListDocenteView

from views.dashboard.modules.PNF import FormularioPNFPensumView
from views.dashboard.modules.tables.PNF.ListarPNF import ListarPNF

from views.dashboard.modules.forms.UnidadCurricular import UnidadCurricular
from views.dashboard.modules.tables.PNF.ListarUC import ListarUC

from views.dashboard.modules.Carga_notas import CargaNotasView
#from views.dashboard.modules.Sedes import ListSedesView

from views.dashboard.modules.Freame_periodos_academicos import PeriodoAcademicoView
from views.dashboard.modules.tables.PeriodosAcademicos.ListPeriodoAcademicoView import ListPeriodoAcademicoView

from views.dashboard.modules.SeccionesView import SeccionView
from views.dashboard.modules.tables.Sedes.ListSedesView import ListSedesView

from views.dashboard.modules.configuracion import Config_user
from views.dashboard.modules.configuracion_sistema import Config_system

from views.dashboard.modules.tables.Secciones.ListadoSeccionesView import ListSeccionesView




class AdminDashboardView(BaseDashboardView):
    
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

        docentes_activos = self.controller['Docentes'].modelo_docente.contar_docentes_activos()
        estudiantes_activos = self.controller['Estudiantes'].modelo.contar_estudiantes_activos()
        pnfs_activos = self.controller['PNF'].modelo.contar_pnf()

        # Mostrar bienvenida usando el componente LabelBienvenida
        bienvenida = LabelBienvenida(self.cuerpo_principal)
        bienvenida.pack(fill="x", padx=10, pady=10)
        bienvenida.configurar(
            titulo="Panel de Control del Administrador",
            mensaje="Desde aquí puedes supervisar y gestionar todos los aspectos del sistema. Los indicadores clave muestran un crecimiento constante.\n¡Tu labor es fundamental para el éxito de nuestra institución!",
            icono_path=ruta,
            alineacion="center"
        )
            # Información de las tarjetas
        cards_info1 = [
            ("Estudiantes Activos", estudiantes_activos, Settings().rutas_iconos.get("estudiantes_icon", "resources/icons/estudiantes.png")),
            ("Docentes Activos", docentes_activos, Settings().rutas_iconos.get("docentes_icon", "resources/icons/docentes.png")),
            ("Cursos Disponibles", pnfs_activos, None),
        ]
        # Crear una CardDisplay
        card_display_frame = ctk.CTkFrame(self.cuerpo_principal, fg_color="transparent")
        card_display_frame.pack(side=ctk.TOP, fill="x", expand=True, pady=20, padx=20)
        
        card_display_frame.grid_columnconfigure(0, weight=1) # Centrar el CardDisplay

        card_display = CardDisplay(card_display_frame, cards_info1)
        card_display.grid(row=0, column=0, sticky="nsew")

 
    def estudiantes(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        estudiantes = FormularioEstudianteView(self.cuerpo_principal, self.controller['Estudiantes'])
        estudiantes.pack(fill="both", expand=True, padx=10, pady=10)
    
    def list_estudiante(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        list_estudiante = ListEstudiantesView(self.cuerpo_principal, self.controller['Estudiantes'],self.controller["Secciones"], self.controller['PNF'], self.user_role, self.username, controllerNotas=self.controller["Notas"])
        list_estudiante.pack(fill="both", expand=True, padx=10, pady=10)
    
    def docentes(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        docentes = FormularioDocenteView(self.cuerpo_principal, self.controller['Docentes'], self.user_role)
        docentes.pack(fill="both", expand=True, padx=10, pady=10)
    
    def list_docente(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        list_docente = ListDocenteView(self.cuerpo_principal, self.controller ,self.user_role, self.username)
        list_docente.pack(fill="both", expand=True, padx=10, pady=10)

    def pnf(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()

        pnf = FormularioPNFPensumView(self.cuerpo_principal, self.controller['PNF'])
        pnf.pack(fill="both", expand=True, padx=10, pady=10)
    
    def unid_Curr(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()

        unid_Curr = UnidadCurricular(self.cuerpo_principal, None, self.controller, mostrar_botones=True, user_name=self.username, rol_user=self.user_role)
        unid_Curr.pack(fill="both", expand=True, padx=10, pady=10)

    def list_pnf(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        # Asegúrate de que el controlador tenga el listado de PNF actualizado
        self.controller['PNF'].actualizar_listado()
        unid_Curr = ListarPNF(self.cuerpo_principal, self.controller["PNF"])
        unid_Curr.pack(fill="both", expand=True, padx=10, pady=10)

    def listar_uc(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        listar_uc = ListarUC(self.cuerpo_principal, self.controller, user_role=self.user_role, username=self.username)
        listar_uc.pack(fill="both", expand=True, padx=10, pady=10)
    
    def carga_notas(self): 
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
                
        carga_notas = CargaNotasView(self.cuerpo_principal, self.controller, user=self.username, rol=self.user_role)
        carga_notas.pack(fill="both", expand=True, padx=10, pady=10)
    
    def periodo(self):
        for widget in self.cuerpo_principal.winfo_children():
             widget.pack_forget()

        periodo_academico = ListPeriodoAcademicoView(self.cuerpo_principal,self.controller["Periodos"])
        periodo_academico.pack(fill="both", expand=True, padx=10, pady=10)
    
    def secciones(self):
        for widget in self.cuerpo_principal.winfo_children():
             widget.pack_forget()

        secciones = SeccionView(self.cuerpo_principal,self.controller["Docentes"],self.controller["PNF"],self.controller["Secciones"],self.controller["Periodos"],self.controller["Sedes"])
        secciones.pack(fill="both", expand=True, padx=10, pady=10)
    
    def sedes(self):
        for widget in self.cuerpo_principal.winfo_children():
             widget.pack_forget()

        sedes = ListSedesView(self.cuerpo_principal, self.controller["Sedes"])
        sedes.pack(fill="both", expand=True, padx=10, pady=10)

    def list_secciones(self):
        for widget in self.cuerpo_principal.winfo_children():
             widget.pack_forget()

        list_secciones = ListSeccionesView(self.cuerpo_principal,self.controller["PNF"],self.controller["Secciones"], self.controller["Docentes"], self.controller["Sedes"], self.controller["Periodos"])
        list_secciones.pack(fill="both", expand=True, padx=10, pady=10)

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
        
    