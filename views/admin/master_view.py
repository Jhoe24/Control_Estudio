import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.admin_base import AdminBase
from views.admin.estudiante_form_view import FormularioEstudianteView
from views.admin.list_estudiante_view import ListEstudiantesView

class VistaMaster(AdminBase):
    def __init__(self, master, controlador, id_usuario):
        super().__init__(master, controlador, id_usuario, titulo="Panel de usuario")
        self.master = master
        self.controlador = controlador
        self.id_usuario = id_usuario 

    def crear_contenido_especifico(self):
        # Por defecto, mostrar inicio
        self.inicio()

    def inicio(self):
        # Limpiar cuerpo y mostrar bienvenida o dashboard
        for w in self.cuerpo_principal.winfo_children(): w.destroy()
        ctk.CTkLabel(self.cuerpo_principal, text="Dashboard de administración",fg_color="black", font=("Roboto",24)).pack(pady=20)

    def estudiantes(self):
        # Limpia el cuerpo principal y muestra la vista del formulario de estudiantes. 
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
            
        self.formulario_estudiante_view = FormularioEstudianteView(self.cuerpo_principal, self.controlador)
        self.formulario_estudiante_view.pack(fill="both", expand=True, padx=10, pady=10)

    def Configuracion(self):
        for w in self.cuerpo_principal.winfo_children(): w.destroy()

        frame = self.cuerpo_principal
        ctk.CTkLabel(frame, text="Configuración de usuario", fg_color="black", font=("Roboto",24)).pack(pady=10)
        
    def list_estudiante(self):
        # Limpia el cuerpo principal y muestra la vista del formulario de estudiantes. 
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
        
        self.list_estudiante_view = ListEstudiantesView(self.cuerpo_principal, self.controlador)
        self.list_estudiante_view.pack(fill="both", expand=True, padx=10, pady=10)