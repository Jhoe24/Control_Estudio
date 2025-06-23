import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from controllers.dashboard.PNF.controller_pnf import ControllerPNF

from ..DatosPersonales import DatosPersonalesFrame

class FrameTramos(SectionFrameBase):
    def __init__(self, master,controlador, vcmd_num, vcmd_fecha, titulo = "Datos Tramos"):
        super().__init__(master, titulo)
        self.controlador = controlador
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

        self.entries_a_validar = [
            self.numero_entry,
            self.nombre_entry,
            self.duracion_semanas_entry,
            self.duracion_horas_entry,
            self.creditos_entry,
            self.objetivos_entry,
            self.estado_option_menu,
        ]

        # Bind para validar campos al escribir
        for entry in self.entries_a_validar:
            entry.bind("<KeyRelease>", lambda event: self.validar_campos_tramo())


    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def procesar_tramo(self):
        return self.controlador.getTramos(self)
    
    
    def validar_campos_tramo(self):
        todos_llenos = all(entry.get().strip() for entry in self.entries_a_validar)
        # Notifica al padre (FrameTrayecto) para que valide el botón global
        if hasattr(self.master.master, "validar_campos_tramos_global"):
            self.master.master.validar_campos_tramos_global()
