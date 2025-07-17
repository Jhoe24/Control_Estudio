# archivo : views/dashboard/modules/forms/Sedes/fromSedes.py
import tkinter.messagebox as messagebox
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class FormSedes(SectionFrameBase):
    def __init__(self, master, controller):
        super().__init__(master, header_text="Gestión de Períodos Académicos")

        self.controller = controller
        
        # Evento de mouse para el formulario
        #self.evento_mouse()

        self.var_estado = tk.StringVar(value="Planificación")  # Variable para el estado del período académico

        self._crear_fila_widgets([
            ("Codigo", crear_entry, {"width": 300, "placeholder_text": "Ingrese el codigo"}, 1, self, "codigo_entry"),
            ("Nombre", crear_entry, {"width": 300, "placeholder_text": "Ingrese el nombre"}, 1, self, "nombre_entry"),
            ("Nombre corto", crear_entry, {"width": 300, "placeholder_text": "Ingrese el nombre corto"}, 1, self, "nombre_corto_entry"),
            ("Tipo", crear_entry, {"width": 300, "placeholder_text": "Ingrese el tipo"}, 1, self, "tipo_entry"),
            ("Dirección", crear_entry, {"width": 300, "placeholder_text": "Ingrese la dirección"}, 1, self, "direccion_entry"),
            ("Teléfono", crear_entry, {"width": 300, "placeholder_text": "Ingrese el teléfono"}, 1, self, "telefono_entry"),
            ("Correo electrónico", crear_entry, {"width": 300, "placeholder_text": "Ingrese el correo electrónico"}, 1, self, "correo_entry"),
            ("Director", crear_entry, {"width": 300, "placeholder_text": "Ingrese el nombre del director"}, 1, self, "director_entry"),
            ("Coordinador_Academico", crear_entry, {"width": 300, "placeholder_text": "Ingrese el nombre del coordinador académico"}, 1, self, "coordinador_academico_entry"),
            ("Estado", crear_option_menu, {"values": ["Planificación", "Inscripción", "En Curso", "Evaluaciones", "Finalizado", "Cerrado"], "variable": self.var_estado, "width": 200}, 1, self, "estado_menu"),
            ("Observación", crear_entry, {"width": 300, "placeholder_text": "Ingrese observaciones"}, 1, self, "observacion_entry")
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
    

    def habilitar_campos(self):
        self.codigo_entry.configure(state="normal")
        self.nombre_entry.configure(state="normal")
        self.nombre_corto_entry.configure(state="normal")
        self.tipo_entry.configure(state="normal")
        self.direccion_entry.configure(state="normal")
        self.telefono_entry.configure(state="normal")
        self.correo_entry.configure(state="normal")
        self.director_entry.configure(state="normal")
        self.coordinador_academico_entry.configure(state="normal")
        self.estado_menu.configure(state="normal")
        self.observacion_entry.configure(state="normal")
        
    def deshabilitar_campos(self):
        self.codigo_entry.configure(state="disabled")
        self.nombre_entry.configure(state="disabled")
        self.nombre_corto_entry.configure(state="disabled")
        self.tipo_entry.configure(state="disabled")
        self.direccion_entry.configure(state="disabled")
        self.telefono_entry.configure(state="disabled")
        self.correo_entry.configure(state="disabled")
        self.director_entry.configure(state="disabled")
        self.coordinador_academico_entry.configure(state="disabled")
        self.estado_menu.configure(state="disabled")
        self.observacion_entry.configure(state="disabled")