import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

# Clase para el filtrado y búsqueda de estudiantes
class FiltradoBusquedaFrame(SectionFrameBase):
    def __init__(self, master,controlador ,vcmd_num):
        super().__init__(master, header_text="Filtrado y Búsqueda")
        self.tipo_documento_var = ctk.StringVar(value="cedula")
        self.vcmd_num = vcmd_num
        self.controlador = controlador
        
        self.frame_tipo_numero_doc = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tipo_numero_doc.pack(fill="x", pady=PADY_FILA, padx=15)

        radio_button_container = ctk.CTkFrame(self.frame_tipo_numero_doc, fg_color="transparent")
        radio_button_container.grid(row=0, column=1, sticky="w", padx=(0,15))
        
        self.radio_cedula = crear_radio_button(radio_button_container, text="Cédula", variable=self.tipo_documento_var, value="cedula")
        self.radio_cedula.pack(side="left", padx=(0, 5), pady=0)

        self.radio_pasaporte = crear_radio_button(radio_button_container, text="Pasaporte", variable=self.tipo_documento_var, value="pasaporte")
        self.radio_pasaporte.pack(side="left", padx=(0, 5), pady=0)
    
        self.nro_documento_entry = crear_entry(self.frame_tipo_numero_doc, width=120, validate="key", validatecommand=(self.vcmd_num, "%S"))
        self.nro_documento_entry.grid(row=0, column=3, sticky="ew", padx=PADX_ENTRY)
        self.frame_tipo_numero_doc.grid_columnconfigure(1, weight=100)
        
        

        self.boton_buscar = ctk.CTkButton(
            self.frame_tipo_numero_doc,
            text="Buscar",
            command=self.ejecutar_busqueda  
        )
        self.boton_buscar.grid(row=0, column=4, padx=10)

    def ejecutar_busqueda(self):
        
        tipo_documento = self.tipo_documento_var.get()
        nro_documento = self.nro_documento_entry.get()
        print(f"tipo de documeto {tipo_documento} : documento de identidad {nro_documento}")
        dic_estudiante=self.controlador.buscar_estudiante(tipo_documento, nro_documento)
        if dic_estudiante:
            self.master.mostrar_resultado_busqueda([dic_estudiante])
        
            

    # def ver_datos_completos(self, estudiante):
    #     """
    #     Muestra una ventana emergente con todos los datos completos de un estudiante, con scroll.
    #     """
    #     ventana = ctk.CTkToplevel(self)
    #     ventana.title("Datos del Estudiante")
    #     ventana.geometry("500x600")
    #     ventana.grab_set()  # Hace que la ventana sea modal

    #     # Usar un CTkScrollableFrame para el contenido
    #     frame = ctk.CTkScrollableFrame(ventana)
    #     frame.pack(fill="both", expand=True, padx=20, pady=20)

    #     etiquetas = {
    #         'tipo_documento': 'Tipo de Documento',
    #         'documento_identidad': 'Número de Documento',
    #         'nombres': 'Nombres',
    #         'apellidos': 'Apellidos',
    #         'codigo_unico': 'Código SNI',
    #         'condicion': 'Condición',
    #         'correo_electronico': 'Correo Electrónico',
    #         'direccion_completa': 'Dirección',
    #         'estado': 'Estado',
    #         'estado_civil': 'Estado Civil',
    #         'fecha_grado_bachiller': 'Fecha Grado Bachiller',
    #         'fecha_grado_profesional': 'Fecha Grado Profesional',
    #         'fecha_ingreso': 'Fecha Ingreso',
    #         'fecha_nacimiento': 'Fecha de Nacimiento',
    #         'fecha_registro': 'Fecha de Registro',
    #         'institucion_procedencia': 'Institución de Procedencia',
    #         'lugar_nacimiento': 'Lugar de Nacimiento',
    #         'mencion_bachiller': 'Mención Bachiller',
    #         'nacionalidad': 'Nacionalidad',
    #         'profesion': 'Profesión',
    #         'sexo': 'Sexo',
    #         'situacion_academica': 'Situación Académica',
    #         'telefonos': 'Teléfonos',
    #         'tipo': 'Tipo',
    #     }

    #     row = 0
    #     for clave, etiqueta in etiquetas.items():
    #         valor = estudiante.get(clave, "")
    #         if clave == "telefonos":
    #             valor = ", ".join(valor) if valor else "No registrado"
    #         elif valor is None:
    #             valor = "No registrado"
    #         ctk.CTkLabel(frame, text=f"{etiqueta}:", font=ctk.CTkFont(weight="bold")).grid(row=row, column=0, sticky="w", pady=2)
    #         ctk.CTkLabel(frame, text=str(valor)).grid(row=row, column=1, sticky="w", pady=2)
    #         row += 1

    #     ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)