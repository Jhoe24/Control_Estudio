import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.admin_base import AdminBase
from views.admin.estudiante_form_view import FormularioEstudianteView
from views.admin.list_estudiante_view import ListEstudiantesView
from views.admin.docente_form_view import FormularioDocenteView
from views.admin.list_docente_view import ListDocenteView

class VistaMaster(AdminBase):
    def __init__(self, master, controlador, id_usuario):
        self.master = master
        self.controlador = controlador
        self.id_usuario = id_usuario 
        
        self.vistas = {}
        
        super().__init__(master, controlador, id_usuario, titulo="Panel de usuario")

        self.vistas['inicio'] = ctk.CTkLabel(self.cuerpo_principal, text="Dashboard de administración", fg_color="black", font=("Roboto",24))
        self.vistas['estudiantes'] = FormularioEstudianteView(self.cuerpo_principal, self.controlador)
        self.vistas['docentes'] = FormularioDocenteView(self.cuerpo_principal, self.controlador)
        self.vistas['list_estudiante'] = ListEstudiantesView(self.cuerpo_principal, self.controlador)
        self.vistas['list_docente'] = ListDocenteView(self.cuerpo_principal, self.controlador)
        self.vistas['configuracion'] = ctk.CTkLabel(self.cuerpo_principal, text="Configuración de usuario", fg_color="black", font=("Roboto",24))

        self.mostrar_vista('inicio')

    def mostrar_vista(self, nombre):
        # Oculta todo
        for widget in self.cuerpo_principal.winfo_children():
            widget.pack_forget()
        # Muestra la vista deseada
        vista = self.vistas.get(nombre)
        if vista:
            if nombre == "list_docente":
                vista.docente = self.controlador.master_controlador.docente.obtener_lista_docentes(0)
            vista.pack(fill="both", expand=True, padx=10, pady=10)

    def crear_contenido_especifico(self):
        self.mostrar_vista('inicio')
    
    def inicio(self):
        self.mostrar_vista('inicio')
        
    def estudiantes(self):
        self.mostrar_vista('estudiantes')

    def docente(self):
        self.mostrar_vista('docentes')

    def Configuracion(self):
        self.mostrar_vista('configuracion')
        
    def list_estudiante(self):
        self.mostrar_vista('list_estudiante')
    
    def list_docente(self):
        self.mostrar_vista('list_docente')