import customtkinter as ctk
from views.auth.base_auth_visual import BaseAuthVisualView
from views.dashboard.components.widget_utils import *
import tkinter.messagebox as messagebox


class RegisterPersonalView(BaseAuthVisualView):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, titulo="Registrar Usuario", es_login=False, **kwargs)

    def crear_contenido_especifico(self):
        self.crear_titulo("Registrar Nuevo Usuario")

        # Campos de entrada
        self.var_tipo_documento = ctk.StringVar(value="cedula")
        self.var_sexo = ctk.StringVar(value="Masculino")
        self.var_tipo_usuario = ctk.StringVar(value="Docente")
        self.var_documento = ctk.StringVar()

        self.radio_cedula = create_option_menu_row(self.frame_contenido, "Cédula", ["cedula", "pasaporte"], self.var_tipo_documento, text_color_="White")
        self.entry_documento = self.crear_campo(self.frame_contenido, "Documento de Identidad:", textvariable_= self.var_documento)
        # Botón Registrar
        self.button_registrar = ctk.CTkButton(
            self.frame_contenido, text="   Siguiente   ", command=self.next
        )
        self.button_registrar.pack(fill=ctk.X, padx=20, pady=(15, 10))

        # Botón Volver
        self.button_volver = ctk.CTkButton(
            self.frame_contenido, text="Volver", command=self.controller["Mostrar_Ventanas"].mostrar_vista_login
        )
        self.button_volver.pack(fill=ctk.X, padx=20, pady=0)

    def campos_necesario(self):

        self.entry_nombre = self.crear_campo(self.frame_contenido, "Nombres:")
        self.entry_apellido = self.crear_campo(self.frame_contenido, "Apellido:")
        self.entry_sexo = create_option_menu_row(self.frame_contenido, "Sexo:",["Masculino", "Femenino"], self.var_sexo, text_color_="White")
        self.menu_tipo = create_option_menu_row(
            self.frame_contenido, "Tipo de Usuario:", ["Docente", "Estudiante"], self.var_tipo_usuario,text_color_="White"
        )

    def registrar_usuario(self):
        # Aquí se obtienen los datos de los campos

        if self.var_sexo.get() == "Masculino":  
            sexo = "M"
        else :
            sexo = "F"


        dic_date = {
            'documento_identidad': self.var_documento.get(),
            'tipo_documento': self.var_tipo_documento.get(),
            'nombre': self.entry_nombre.get(),
            'apellido': self.entry_apellido.get(),
            'fecha_nacimiento': '',  # Este campo debe ser llenado en otro formulario
            'sexo': sexo,
            'estado_civil': None,  # Este campo debe ser llenado en otro formulario
            'nacionalidad': '',  # Este campo debe ser llenado en otro formulario
            'lugar_nacimiento': '',  # Este campo debe ser llenado en otro formulario
            'correo_electronico': '',  # Este campo debe ser llenado en otro formulario
            'fecha_registro': '',  # Este campo debe ser llenado automáticamente
            'genero': self.var_tipo_usuario.get(),
            'tipo': self.var_tipo_usuario.get().lower(),
            'estado': "activo",  # Activo por defecto
        }

        if not dic_date['documento_identidad'] or not dic_date['nombre'] or not dic_date['apellido']:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        persona_id = self.controller["LoginAuth"].register_person(dic_date)
        if persona_id:
            self.controller["Mostrar_Ventanas"].mostrar_vista_registro(persona_id)
        else:
            messagebox.showerror("Error", "No se pudo registrar la persona. Verifica los datos e intenta nuevamente.")
        
    def validarCampo(self, text):
        return text.isdecimal() and len(text) <= 8 or text == ""
    
    def next(self):
        tipo_documento = self.var_tipo_documento.get()
        documento = self.var_documento.get()
        if not documento :
            messagebox.showerror("Error", "El campo de documento es obligatorio y debe ser numérico.")
            return
        else:
            
            if not self.controller["LoginAuth"].exists_personal(tipo_documento, documento): 
                print("usuario aun no registrado")
                self.campos_necesario()
                self.entry_documento.configure(state="disabled")
                self.radio_cedula.configure(state="disabled")
                self.button_registrar.configure(text="Registrar", command=self.registrar_usuario)
                self.button_volver.configure(text="Cancelar", command=self.controller["Mostrar_Ventanas"].mostrar_vista_login)
                #Reposicionar los botones 10123456
                self.button_registrar.pack_forget()
                self.button_volver.pack_forget()
                self.button_registrar.pack(fill=ctk.X, padx=20, pady=(15, 10))
                self.button_volver.pack(fill=ctk.X, padx=20, pady=0)
            else:
                if self.controller["LoginAuth"].exists_user(tipo_documento, documento):
                    messagebox.showerror("Error", "Esta persona ya posee un usuario.")
                    self.button_registrar.configure(state="disabled")
                    return
                else:
                    #obtener el id de la persona
                    result = self.controller["LoginAuth"].search_document(tipo_documento, documento)
                    if result:
                        persona_id = result[0]
                    else:
                        messagebox.showerror("Error", "Ha ocurrido un error inesperado intente de nuevo.")
                        return
                    self.controller["Mostrar_Ventanas"].mostrar_vista_registro(persona_id)

    def on_entry_change(self,*args):
        print(f"El valor del Entry cambió a: {self.var_documento.get()}")