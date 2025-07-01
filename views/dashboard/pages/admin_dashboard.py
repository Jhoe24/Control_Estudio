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


class AdminDashboardView(BaseDashboardView):
    
    def __init__(self, master, controller, username, user_role, **kwargs):
        super().__init__(master, controller, username, user_role, **kwargs)
        self.master = master
        self.controller = controller
        
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
            titulo="¡Bienvenido al Panel de Control del Administrador!",
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

 
    def estudiantes(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        estudiantes = FormularioEstudianteView(self.cuerpo_principal, self.controller['Estudiantes'])
        estudiantes.pack(fill="both", expand=True, padx=10, pady=10)
    
    def list_estudiante(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        list_estudiante = ListEstudiantesView(self.cuerpo_principal, self.controller['Estudiantes'])
        list_estudiante.pack(fill="both", expand=True, padx=10, pady=10)
    
    def docentes(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        docentes = FormularioDocenteView(self.cuerpo_principal, self.controller['Docentes'])
        docentes.pack(fill="both", expand=True, padx=10, pady=10)
    
    def list_docente(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        list_docente = ListDocenteView(self.cuerpo_principal, self.controller['Docentes'])
        list_docente.pack(fill="both", expand=True, padx=10, pady=10)

    def pnf(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()

        pnf = FormularioPNFPensumView(self.cuerpo_principal, self.controller['PNF'])
        pnf.pack(fill="both", expand=True, padx=10, pady=10)
    
    def unid_Curr(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()

        unid_Curr = UnidadCurricular(self.cuerpo_principal, None, controlador= None)
        unid_Curr.pack(fill="both", expand=True, padx=10, pady=10)

    def list_pnf(self):
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        
        # Asegúrate de que el controlador tenga el listado de PNF actualizado
        self.controller['PNF'].actualizar_listado()
        unid_Curr = ListarPNF(self.cuerpo_principal, self.controller["PNF"])
        unid_Curr.pack(fill="both", expand=True, padx=10, pady=10)
