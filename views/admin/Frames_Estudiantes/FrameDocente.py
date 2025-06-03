# abreviatura de titulo
# especialidad
# fecha de ingreso
# tipo de contrato
# categoria
# auxiliar
# dedicacion
# estado
# importacion de la libreria customTkinter
import customtkinter as ctk
from util.widget_utils import *
from views.layouts.SectionFrameBase import SectionFrameBase
from .DatosPersonales import DatosPersonalesFrame

class FrameDocente(SectionFrameBase):
    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, header_text="Datos del Docente")
        self.vcmd_num = vcmd_num
        self.vcmd_fecha = vcmd_fecha
        self.var_abre_titulo = ctk.StringVar(value='Prof.')  # Valor por defecto para la abreviatura del título
        self.var_tipo_contrato = ctk.StringVar(value='Tiempo completo')  # Valor por defecto para el tipo de contrato
        self.var_dedicacion = ctk.StringVar(value='Exclusiva')  # Valor por defecto para la dedicación
        self._crear_fila_widgets([
            ("Abreviatura de Título:", crear_option_menu, {"values":["Prof.", "Ing.", "Lic.", "Abog.", "TSU.", "Otros"],'variable': self.var_abre_titulo,"command": lambda v: setattr(self.abreviatura_menu, '_current_value',v)}, 1, self, 'abreviatura_menu'),
            ("Especialidad:", crear_entry, {"width":220}, 1, self, 'especialidad_entry')
        ])
        #("Cédula:", crear_entry, {"width":220, "validate":"key", "validatecommand":(vcmd_num, '%P')}, 1, self, 'cedula_entry')
        self._crear_fila_widgets([
            ("Fecha Ingreso:", crear_entry, {"width":120,"placeholder_text":"dd-mm-aaaa"}, 1, self, 'fecha_ingreso_entry'),
            ("Tipo de Contrato:", crear_option_menu, {"values":["Tiempo completo", "Medio tiempo", "Por horas", "Contratado"],"variable": self.var_tipo_contrato, "command": lambda v: setattr(self.tipo_contrato_menu, '_current_value',v)}, 1, self, 'tipo_contrato_menu')
        ])

        self._crear_fila_widgets([
            ("Categoría", crear_entry, {"width":220}, 1, self, 'categoria_entry'),
            ("Auxiliar:", crear_option_menu, {"values":["Si", "No"], "command": lambda v: setattr(self.auxiliar_menu, '_current_value',v)}, 1, self, 'auxiliar_menu')
        ])

        self._crear_fila_widgets([
            ("Dedicación:", crear_option_menu, {"values":["Exclusiva", "Tiempo completo", "Medio tiempo", "Tiempo convencional"],"variable": self.var_dedicacion,"command": lambda v: setattr(self.dedicacion_menu, '_current_value',v)}, 1, self, 'dedicacion_menu'),
            ("Estado:", crear_option_menu, {"values":["Activo", "Inactivo", "Jubilado", "Permiso"], "command": lambda v: setattr(self.estado_doc_menu, '_current_value',v)}, 1, self, 'estado_doc_menu')
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def set_datos(self, docente):
        # asignar valores y deshabilitar campos
        self.abreviatura_menu.set(self.var_abre_titulo.get())
        self.abreviatura_menu.configure(state="disabled")
        
        # Configurar especialidad
        self.especialidad_entry.delete(0, ctk.END)
        if docente.get('especialidad') is not None and docente.get('especialidad') != "":
            self.especialidad_entry.insert(0, docente.get("especialidad"))
        self.especialidad_entry.configure(state="disabled")

        # Configurar fecha de ingreso
        self.fecha_ingreso_entry.delete(0, ctk.END)
        if docente.get('fecha_ingreso') is not None and docente.get('fecha_ingreso') != "":
            self.fecha_ingreso_entry.insert(0, docente.get("fecha_ingreso"))
        self.fecha_ingreso_entry.configure(state="disabled")

        # Configurar tipo de contrato
        self.tipo_contrato_menu.set(self.var_tipo_contrato.get())
        self.tipo_contrato_menu.configure(state="disabled")

        # Configurar categoría
        self.categoria_entry.delete(0, ctk.END)
        if docente.get('categoria') is not None and docente.get('categoria') != "":
            self.categoria_entry.insert(0, docente.get("categoria"))
        self.categoria_entry.configure(state="disabled")

        # Configurar auxiliar
        self.auxiliar_menu.set("Si" if docente.get('auxiliar') else "No")
        self.auxiliar_menu.configure(state="disabled")

        # Configurar dedicación
        self.dedicacion_menu.set(self.var_dedicacion.get())
        self.dedicacion_menu.configure(state="disabled")

        # Configurar estado del docente
        self.estado_doc_menu.set("Activo" if docente.get('estado_docente') == "Activo" else "Inactivo")
        self.estado_doc_menu.configure(state="disabled")

    # Método para habilitar la edición de los campos sin eliminar el contenido
    def habilitar_edicion(self):
        self.abreviatura_menu.configure(state="normal")
        self.especialidad_entry.configure(state="normal")
        self.fecha_ingreso_entry.configure(state="normal")
        self.tipo_contrato_menu.configure(state="normal")
        self.categoria_entry.configure(state="normal")
        self.auxiliar_menu.configure(state="normal")
        self.dedicacion_menu.configure(state="normal")
        self.estado_doc_menu.configure(state="normal")
    