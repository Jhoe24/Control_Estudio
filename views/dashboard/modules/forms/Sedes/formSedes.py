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


    def cargar_datos(self, datos):
        try:
            # Código Entry
            self.codigo_entry.delete(0, "end")
            codigo_val = datos.get("codigo", "")
            if codigo_val: # Solo inserta si no es nulo o cadena vacía
                self.codigo_entry.insert(0, codigo_val)
            self.codigo_entry.configure(state="disabled")

            # Nombre Entry
            self.nombre_entry.delete(0, "end")
            nombre_val = datos.get("nombre", "")
            if nombre_val: # Solo inserta si no es nulo o cadena vacía
                self.nombre_entry.insert(0, nombre_val)
            self.nombre_entry.configure(state="disabled")

            # Nombre Corto Entry
            self.nombre_corto_entry.delete(0, "end")
            nombre_corto_val = datos.get("nombre_corto", "")
            if nombre_corto_val: # Solo inserta si no es nulo o cadena vacía
                self.nombre_corto_entry.insert(0, nombre_corto_val)
            self.nombre_corto_entry.configure(state="disabled")

            # Tipo Entry
            self.tipo_entry.delete(0, "end")
            tipo_val = datos.get("tipo", "")
            if tipo_val: # Solo inserta si no es nulo o cadena vacía
                self.tipo_entry.insert(0, tipo_val)
            self.tipo_entry.configure(state="disabled")

            # Dirección Entry
            self.direccion_entry.delete(0, "end")
            direccion_val = datos.get("direccion", "")
            if direccion_val: # Solo inserta si no es nulo o cadena vacía
                self.direccion_entry.insert(0, direccion_val)
            self.direccion_entry.configure(state="disabled")

            # Teléfono Entry
            self.telefono_entry.delete(0, "end")
            telefono_val = datos.get("telefono", "")
            if telefono_val: # Ya tenías esta validación, la mantengo
                self.telefono_entry.insert(0, str(telefono_val))
            self.telefono_entry.configure(state="disabled")

            # Correo Entry
            self.correo_entry.delete(0, "end")
            correo_val = datos.get("correo", "")
            if correo_val: # Solo inserta si no es nulo o cadena vacía
                self.correo_entry.insert(0, correo_val)
            self.correo_entry.configure(state="disabled")

            # Director Entry
            self.director_entry.delete(0, "end")
            director_val = datos.get("director", "")
            if director_val: # Solo inserta si no es nulo o cadena vacía
                self.director_entry.insert(0, director_val)
            self.director_entry.configure(state="disabled")

            # Coordinador Académico Entry
            self.coordinador_academico_entry.delete(0, "end")
            coordinador_academico_val = datos.get("coordinador_academico", "")
            if coordinador_academico_val: # Solo inserta si no es nulo o cadena vacía
                self.coordinador_academico_entry.insert(0, coordinador_academico_val)
            self.coordinador_academico_entry.configure(state="disabled")

            # Observación Entry
            self.observacion_entry.delete(0, "end")
            observacion_val = datos.get("observaciones", "")
            if observacion_val: # Solo inserta si no es nulo o cadena vacía
                self.observacion_entry.insert(0, observacion_val)
            self.observacion_entry.configure(state="disabled")

            # Estado Menu
            self.var_estado.set(datos.get("estado", "Planificación"))
            self.estado_menu.configure(state="disabled")

        except Exception as e:
            print(f"Error al cargar datos en el formulario: {e}")

                