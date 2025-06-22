import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame

from config.app_config import AppConfig


class UnidadCurricular(SectionFrameBase):
    def __init__(self, master, vcmd_num):
        super().__init__(master, "Unidad Curricular PNF")
        self.vcmd_num = vcmd_num # Guardar para usar en números
        #self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
              
        # Filas de Datos para el formulario de Unidad Curricular PNF

        # Fila para los datos de la Unidad Curricular

        self._crear_fila_widgets([
            ("Código:", crear_entry, {"width":300,"placeholder_text":"Ingrese código"}, 1, self.scroll, 'codigo_entry'),
            ("Nombre:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre de la U.C"}, 1, self.scroll, 'nombre_entry'),
            ("Nombre corto:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre corto"}, 1, self.scroll, 'nombre_corto_entry'),
            ("Área:", crear_entry, {"width":300,"placeholder_text":"Ingrese área"}, 1, self.scroll, 'area_entry'),
            ("Sub-area:", crear_entry, {"width":300,"placeholder_text":"Ingrese Sub-area"}, 1, self.scroll, 'subarea_entry'),
            ("Eje Formativo:", crear_entry, {"width":300,"placeholder_text":"Ingrese el eje formativo"}, 1, self.scroll, 'eje_formativo_entry'),
        ], es_scroll=True)
        
        # Fila para las horas de la Unidad Curricular
        self._crear_fila_widgets([
            ("Horas Teóricas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_teoricas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Prácticas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_practicas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Laboratorio:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_laboratorio_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Trabajo Pendiente:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_trabajo_independiente_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Totales:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_totales_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
        ], es_scroll=True)

        # Fila para otros datos de la Unidad Curricular
        self._crear_fila_widgets([
            ("Unidad de Crédito:", crear_entry, {"width":300,"placeholder_text":"Ingrese Unidad de crédito"}, 1, self.scroll, 'unidades_credito_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Tipo de U.C:", crear_option_menu, {"values": ["Obligatoria", "Electiva"], "width":300}, 1, self.scroll, 'tipo_menu'),
            ("Carácter:", crear_option_menu, {"values": ["Teórico", "Práctico", "Teórico-Práctico"], "width":300}, 1, self.scroll, 'caracter_menu'),
            ("Modalidad de Evaluación:", crear_option_menu, {"values": ["Presencial", "Semi-presencial", "A distancia"], "width":300}, 1, self.scroll, 'modalidad_menu'),
            ("Complejidad:", crear_option_menu, {"values": ["Baja", "Media", "Alta"], "width":300}, 1, self.scroll, 'complejidad_menu'),
            ("Prelaciones:", crear_entry, {"width": 300, "placeholder_text": "Ingrese prelaciones"}, 1, self.scroll, 'prelaciones_entry'),
        ], es_scroll=True)

        # Fila para competencias y saberes
        self._crear_fila_widgets([
            ("Competencias Genéricas:", crear_entry, {"width": 300, "placeholder_text": "Ingrese competencias genéricas"}, 1, self.scroll, 'competencias_genericas_entry'),
            ("Competencias Específicas:", crear_entry, {"width": 300, "placeholder_text": "Ingrese competencias específicas"}, 1, self.scroll, 'competencias_especificas_entry'),
        ], es_scroll=True)
        self._crear_fila_widgets([
            ("Saberes Cognitivos:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes cognitivos"}, 1, self.scroll, 'saberes_cognitivos_entry'),
            ("Saberes Procedimentales:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes procedimentales"}, 1, self.scroll, 'saberes_procedimentales_entry'),
            ("Saberes Actitudinales:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes actitudinales"}, 1, self.scroll, 'saberes_actitudinales_entry'),
        ], es_scroll=True)

        # Fila para estrategias, recursos y evaluación
        self._crear_fila_widgets([
            ("Estrategias de Enseñanza:", crear_entry, {"width": 300, "placeholder_text": "Ingrese estrategias de enseñanza"}, 1, self.scroll, 'estrategias_ensenanza_entry'),
            ("Recursos Didácticos:", crear_entry, {"width": 300, "placeholder_text": "Ingrese recursos didácticos"}, 1, self.scroll, 'recursos_didacticos_entry'),
            ("Evaluación:", crear_entry, {"width": 300, "placeholder_text": "Ingrese criterios de evaluación"}, 1, self.scroll, 'evaluacion_entry'),
        ], es_scroll=True)

        # Fila para bibliografía, homologación y clave especial
        self._crear_fila_widgets([
            ("Bibliografía:", crear_entry, {"width": 300, "placeholder_text": "Ingrese bibliografía"}, 1, self.scroll, 'bibliografia_entry'),
            ("Homologación Clave:", crear_entry, {"width": 300, "placeholder_text": "Ingrese clave de homologación"}, 1, self.scroll, 'homologacion_clave_entry'),
            ("Clave Especial:", crear_entry, {"width": 300, "placeholder_text": "Ingrese clave especial"}, 1, self.scroll, 'clave_especial_entry'),
        ], es_scroll=True)

        # Fila para estado y fechas
        self._crear_fila_widgets([
            ("Estado:", crear_option_menu, {"values": ["Activo", "Inactivo"], "width": 300}, 1, self.scroll, 'estado_menu'),
            ("Fecha de Creación:", crear_entry, {"width": 300, "placeholder_text": "YYYY-MM-DD"}, 1, self.scroll, 'fecha_creacion_entry'),
            ("Fecha de Actualización:", crear_entry, {"width": 300, "placeholder_text": "YYYY-MM-DD"}, 1, self.scroll, 'fecha_actualizacion_entry'),
        ], es_scroll=True)

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
