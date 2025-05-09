import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.admin_base import AdminBase

class VistaMaster(AdminBase):
    def __init__(self, master, controlador, id_usuario):
        super().__init__(master, controlador, id_usuario, titulo="Panel de usuario")

    def crear_contenido_especifico(self):
        # Por defecto, mostrar inicio
        self.inicio()

    def inicio(self):
        # Limpiar cuerpo y mostrar bienvenida o dashboard
        for w in self.cuerpo_principal.winfo_children(): w.destroy()
        ctk.CTkLabel(self.cuerpo_principal, text="Dashboard de administración",fg_color="black", font=("Roboto",24)).pack(pady=20)

    def estudiantes(self):
        for w in self.cuerpo_principal.winfo_children(): w.destroy()
        ctk.CTkLabel(self.cuerpo_principal, text="Gestión de estudiantes",fg_color="black", font=("Roboto",24)).pack(pady=20)

    def _mostrar_ayuda(self):
        for w in self.cuerpo_principal.winfo_children(): w.destroy()
        ctk.CTkLabel(self.cuerpo_principal, text="Sección de ayuda", font=("Roboto",24)).pack(pady=20)

    def Configuracion(self):
        for w in self.cuerpo_principal.winfo_children(): w.destroy()

        frame = self.cuerpo_principal
        ctk.CTkLabel(frame, text="Configuración de usuario", fg_color="black", font=("Roboto",24)).pack(pady=10)
        
