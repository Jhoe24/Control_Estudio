import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

from ..DatosPersonales import DatosPersonalesFrame

class FrameTrayecto(SectionFrameBase):
    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, header_text="Datos de Trayecto")
        self.vcmd_num = vcmd_num 
        self.var = ctk.StringVar()
        self.var.set("Activo")  # Valor por defecto para el estado
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        # --- Fila para los datos de Trayecto ---
        self._crear_fila_widgets([
            ("Número:", crear_entry, {"width":300,"placeholder_text":"Ingrese número"}, 1, self, 'numero_entry'),
            ("Nombre:", crear_entry, {"width":360,"placeholder_text":"Ingrese nombre"}, 1, self, 'nombre_entry'),
            ("Tipo:", crear_entry, {"width":300, "placeholder_text":"Tipo de Trayecto"}, 1, self, 'tipo_entry')
        ])

        # --- Fila para información de Trayecto ---
        self._crear_fila_widgets([
            ("Duración en semanas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_semanas_entry'),
            ("Duración en horas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_horas_entry'),
            ("Créditos Mínimos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_minimos_entry'),
            ("Créditos Máximos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_maximos_entry'),
            ("Número de Tramos:", crear_entry, {"width":300,"placeholder_text":"Ingrese número de tramos"}, 1, self, 'numero_tramos_entry')
        ])

        # --- Fila para información adicional de Trayecto ---
        self._crear_fila_widgets([
            ("Objetivos:", crear_entry, {"width":300,"placeholder_text":"Ingrese objetivos"}, 1, self, 'objetivos_entry'),
            ("Competencias:", crear_entry, {"width":300,"placeholder_text":"Ingrese competencias"}, 1, self, 'competencias_entry'),
            ("Perfil de Egreso:", crear_entry, {"width":300,"placeholder_text":"Ingrese perfil de egreso"}, 1, self, 'perfil_egreso_entry'),
            ("Obligatorio:", crear_option_menu, {"values":["Si", "No"], "command": lambda v: setattr(self.obligatorio_menu, '_current_value',v)}, 1, self, 'obligatorio_menu'),
            ("Secuencial:", crear_option_menu, {"values":["Si", "No"], "command": lambda v: setattr(self.secuencial_menu, '_current_value',v)}, 1, self, 'secuencial_menu'),
            ("Estado:", crear_option_menu, {"values":["Activo", "Inactivo"], "command": lambda v: setattr(self.estado_menu, '_current_value',v)}, 1, self, 'estado_menu')
        ])

        # --- Fila para duración del trayecto ---
        self.label_duracion_contenedor = ctk.CTkLabel(self, text="Duración del Trayecto (en horas y semanas):")
        self.label_duracion_contenedor.pack(anchor="w", padx=PADX_LABEL, pady=PADY_FILA)
        self.duracion_trayectos_entry = ctk.CTkEntry(self.label_duracion_contenedor,
                                                     width=300, placeholder_text="Ingrese duración de horas")
        self.duracion_trayectos_entry.grid(row=0, column=1, padx=PADX_LABEL, pady=PADY_FILA, sticky="w")

        self.duracion_semanas_entry = ctk.CTkEntry(self.label_duracion_contenedor,
                                                     width=300, placeholder_text="Ingrese duración de semanas")
        self.duracion_semanas_entry.grid(row=0, column=2, padx=PADX_LABEL, pady=PADY_FILA, sticky="w")

