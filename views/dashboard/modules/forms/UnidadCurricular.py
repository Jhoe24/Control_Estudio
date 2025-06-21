import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame

from config.app_config import AppConfig

class UnidadCurricular(SectionFrameBase):
    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, "Unidad Curricular PNF", "Formulario de Unidades Curriculares PNF")
        self.vcmd_num = vcmd_num # Guardar para usar en números
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        self
        
        ventana = ctk.CTkToplevel()
        ventana.title("Formulario de Unidades Curriculares PNF")
        ventana.geometry("850x700") 
        AppConfig().centrar_ventana(ventana, 850, 700)

        ventana.grab_set() # Bloquea la ventana principal

        # Filas de Datos para el formulario de Unidad Curricular PNF
        self._crear_fila_widgets([
            ("Código:", crear_entry, {"width":300,"placeholder_text":"Ingrese código"}, 1, self, 'codigo_entry'),
            ("Nombre:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre de la U.C"}, 1, self, 'nombre_entry'),
            ("Nombre corto:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre corto"}, 1, self, 'nombre_corto_entry'),
            ("Área:", crear_entry, {"width":300,"placeholder_text":"Ingrese área"}, 1, self, 'area_entry'),
            ("Sub-area:", crear_entry, {"width":300,"placeholder_text":"Ingrese Sub-area"}, 1, self, 'subarea_entry'),
            ("Eje Formativo:", crear_entry, {"width":300,"placeholder_text":"Ingrese el eje formativo"}, 1, self, 'eje_formativo_entry'),
        ])

        # Fila para las horas de la Unidad Curricular
        self._crear_fila_widgets([
            ("Horas Teóricas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self, 'horas_teoricas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Prácticas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self, 'horas_practicas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Laboratorio:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self, 'horas_laboratorio_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Trabajo Pendiente:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self, 'horas_trabajo_independiente_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Totales:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self, 'horas_totales_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
        ])

        # Fila para otros datos de la Unidad Curricular
        self._crear_fila_widgets([
            ("Unidad de Crédito:", crear_entry, {"width":300,"placeholder_text":"Ingrese Unidad de crédito"}, 1, self, 'unidades_credito_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Tipo de U.C:", crear_option_menu, {"values": ["Obligatoria", "Electiva"], "width":300}, 1, self, 'tipo_menu'),
            ("Carácter:", crear_option_menu, {"values": ["Teórico", "Práctico", "Teórico-Práctico"], "width":300}, 1, self, 'caracter_menu'),
            ("Modalidad de Evaluación:", crear_option_menu, {"values": ["Presencial", "Semi-presencial", "A distancia"], "width":300}, 1, self, 'modalidad_evaluacion_menu'),
            ("Modalidad:", crear_combobox, {"values": ["Presencial", "Semi-presencial", "A distancia"], "width":300}, 1, self, 'modalidad_combobox'),
            ("Nivel:", crear_combobox, {"values": ["Básico", "Intermedio", "Avanzado"], "width":300}, 1, self, 'nivel_combobox'),
        ])

        # Crear un contenedor scrollable para la ventana emergente
        contenedor_scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_FONDO_FORMULARIO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=10)


        
        
    

