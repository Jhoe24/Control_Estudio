import customtkinter as ctk
from util.mensaje import CustomMessageBox
from views.layouts.admin_base import AdminBase
from views.admin.estudiante_form_view import FormularioEstudianteView

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
        """
        Limpia el cuerpo principal y muestra la vista del formulario de estudiantes.
        """
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
        
        # Accedemos al estudiante_controlador a través de self.controlador
        # (que es la instancia de ControladorPrincipal).
        try:
            controlador_est = self.controlador.estudiante_controlador
        except AttributeError:
            # Esto podría pasar si olvidaste añadir 'estudiante_controlador'
            # como atributo en la clase ControladorPrincipal.
            print("ERROR: ControladorPrincipal no tiene el atributo 'estudiante_controlador'")
            ctk.CTkLabel(self.cuerpo_principal, text="Error: Falta el controlador de estudiantes.",
                         font=("Roboto", 18), text_color="red").pack(pady=20)
            return

        # Instanciamos y mostramos la vista del formulario de estudiantes.
        # Pasamos self.cuerpo_principal como el 'master' donde se dibujará esta vista (frame),
        # y el controlador_est para su lógica.
        self.formulario_estudiante_view = FormularioEstudianteView(self.cuerpo_principal, controlador_est)
        self.formulario_estudiante_view.pack(fill="both", expand=True, padx=10, pady=10)

    def Configuracion(self):
        for w in self.cuerpo_principal.winfo_children(): w.destroy()

        frame = self.cuerpo_principal
        ctk.CTkLabel(frame, text="Configuración de usuario", fg_color="black", font=("Roboto",24)).pack(pady=10)
        
