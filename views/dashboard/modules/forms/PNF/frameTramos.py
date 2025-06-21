import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

from ..DatosPersonales import DatosPersonalesFrame

class FrameTramos(SectionFrameBase):
    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, header_text="Datos de Tramos")
        self.vcmd_num = vcmd_num # Guardar para usar en números
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        
        # -- Fila de Datos del Tramo --
        self._crear_fila_widgets([
            ("Número:", crear_entry, {"width":300,"placeholder_text":"Ingrese número"}, 1, self, 'numero_entry'),
            ("Nombre:", crear_entry, {"width":360,"placeholder_text":"Ingrese nombre"}, 1, self, 'nombre_entry'),
        ])

        # -- Fila de Duración --
        self._crear_fila_widgets([
            ("Duración en semanas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_semanas_entry'),
            ("Duración en horas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_horas_entry'),
        ])

        # -- Fila de información adicional --
        self._crear_fila_widgets([
            ("Créditos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_entry'),
            ("Objetivos:", crear_entry, {"width":300,"placeholder_text":"Ingrese objetivos"}, 1, self, 'objetivos_entry'),
            ("Estado:", crear_option_menu, {"values": ["Activo", "Inactivo"], "width":300}, 1, self, 'estado_option_menu')
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
