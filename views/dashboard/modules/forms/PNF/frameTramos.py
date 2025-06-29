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
            ("Estado:", crear_option_menu, {"values": ["activo", "inactivo"], "width":300}, 1, self, 'estado_option_menu')
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
        todos_llenos = all(str(entry.get()).strip() for entry in self.entries_a_validar)
        # Notifica al padre (FrameTrayecto) para que valide el botón global
        if hasattr(self.master.master, "validar_campos_tramos_global"):
            self.master.master.validar_campos_tramos_global()   


    def set_datos(self, datos):
        self.numero_entry.insert(0, datos.get("numero", ""))
        self.numero_entry.configure(state="disabled")
        self.nombre_entry.insert(0, datos.get("nombre", ""))
        self.nombre_entry.configure(state="disabled")
        self.duracion_semanas_entry.insert(0, datos.get("duracion_semanas", ""))
        self.duracion_semanas_entry.configure(state="disabled")
        self.duracion_horas_entry.insert(0, datos.get("duracion_horas", ""))
        self.duracion_horas_entry.configure(state="disabled")
        self.creditos_entry.insert(0, datos.get("creditos", ""))
        self.creditos_entry.configure(state="disabled")
        self.objetivos_entry.insert(0, datos.get("objetivos", ""))
        self.objetivos_entry.configure(state="disabled")
        # Si tienes un campo para competencias, agrégalo aquí
        if hasattr(self, "competencias_entry"):
            self.competencias_entry.insert(0, datos.get("competencias", ""))
            self.competencias_entry.configure(state="disabled")
        self.estado_option_menu.set(datos.get("estado", "activo"))
        self.estado_option_menu.configure(state="disabled")
    
    def habilitar_campos(self):
        for campo in self.entries_a_validar:
            campo.configure(state="norma")