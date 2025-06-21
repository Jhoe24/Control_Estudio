import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

from ..DatosPersonales import DatosPersonalesFrame

class FrameTrayecto(SectionFrameBase):
    def __init__(self, master,vcmd_num, vcmd_fecha,titulo = "Trayecto"):
        super().__init__(master, titulo )
        self.vcmd_num = vcmd_num 
        self.var = ctk.StringVar()
        self.var.set("Activo")  # Valor por defecto para el estado
        self.var2 = ctk.StringVar()
        self.var2.set("Trayectos de IV")  # Valor por defecto para el tipo
        self.var3 = ctk.StringVar()
        self.var3.set("Soporte Técnico a Usuarios y Equipos")  # Valor por defecto para el perfil de egreso
        self.var4 = ctk.StringVar()
        self.var4.set("Si")  # Valor por defecto para obligatorio
        self.var5 = ctk.StringVar()
        self.var5.set("Si")  # Valor por defecto para secuencial
        self.var6 = ctk.StringVar()
        self.var6.set("Si")  # Valor por defecto para estado
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        
        # --- Fila para los datos de Trayecto ---
        self._crear_fila_widgets([
            ("Número:", crear_entry, {"width":300,"placeholder_text":"Ingrese número"}, 1, self, 'numero_entry'),
            ("Nombre:", crear_entry, {"width":360,"placeholder_text":"Ingrese nombre"}, 1, self, 'nombre_entry'),
            ("Tipo:", crear_option_menu, {"values":["Trayectos de IV", "Trayectos de V"], "command": lambda v: setattr(self.tipo_menu, '_current_value',v)}, 1, self, 'tipo_menu'),
        ])

        # --- Fila para información de Trayecto ---
        self._crear_fila_widgets([
            ("Duración en semanas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_semanas_entry'),
            ("Duración en horas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_horas_entry'),
            ("Créditos Mínimos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_minimos_entry'),
            ("Créditos Máximos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_maximos_entry'),
            ("Número de Tramos:", crear_option_menu, {"values":["1", "2", "3"], "command": lambda v: setattr(self.numero_tramos_menu, '_current_value',v)}, 1, self, 'numero_tramos_menu'),
        ])

        # --- Fila para información adicional de Trayecto ---
        self._crear_fila_widgets([
            ("Objetivos:", crear_entry, {"width":300,"placeholder_text":"Ingrese objetivos"}, 1, self, 'objetivos_entry'),
            ("Perfil de Egreso:", crear_option_menu, {"values":["Soporte Técnico a Usuarios y Equipos", "Técnico Superior Universitario", "Desarrollador de Aplicaciones", "Ingeniero en Informática"], "command": lambda v: setattr(self.perfil_egreso_menu, '_current_value',v)}, 1, self, 'perfil_egreso_menu'),
            ("Obligatorio:", crear_option_menu, {"values":["Si", "No"], "command": lambda v: setattr(self.obligatorio_menu, '_current_value',v)}, 1, self, 'obligatorio_menu'),
            ("Secuencial:", crear_option_menu, {"values":["Si", "No"], "command": lambda v: setattr(self.secuencial_menu, '_current_value',v)}, 1, self, 'secuencial_menu'),
            ("Estado:", crear_option_menu, {"values":["Activo", "Inactivo"], "command": lambda v: setattr(self.estado_menu, '_current_value',v)}, 1, self, 'estado_menu')
        ])
        
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
