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
        
        self._crear_fila_widgets([
            ("Abreviatura de Título:", crear_option_menu, {"values":["Prof.", "Ing.", "Lic.", "Abog.", "TSU.", "Otros"],'variable': self.var_abre_titulo,"command": lambda v: setattr(self.abreviatura_menu, '_current_value',v)}, 1, self, 'abreviatura_menu'),
            ("Especialidad:", crear_entry, {"width":220}, 1, self, 'especialidad_entry')
        ])
        #("Cédula:", crear_entry, {"width":220, "validate":"key", "validatecommand":(vcmd_num, '%P')}, 1, self, 'cedula_entry')
        self._crear_fila_widgets([
            ("Fecha Ingreso:", crear_entry, {"width":120,"placeholder_text":"dd/mm/aaaa"}, 1, self, 'fecha_ingreso_entry'),
            ("Tipo de Contrato:", crear_option_menu, {"values":["Fijo", "Indefinido", "Otro"], "command": lambda v: setattr(self.tipo_contrato_menu, '_current_value',v)}, 1, self, 'tipo_contrato_menu')
        ])

        self._crear_fila_widgets([
            ("Categoría", crear_entry, {"width":220}, 1, self, 'categoria_entry'),
            ("Auxiliar:", crear_option_menu, {"values":["Sí", "No"], "command": lambda v: setattr(self.auxiliar_menu, '_current_value',v)}, 1, self, 'auxiliar_menu')
        ])

        self._crear_fila_widgets([
            ("Dedicación:", crear_option_menu, {"values":["Tiempo Completo", "Medio Tiempo", "Por Horas"], "command": lambda v: setattr(self.dedicacion_menu, '_current_value',v)}, 1, self, 'dedicacion_menu'),
            ("Estado:", crear_option_menu, {"values":["Activo", "Inactivo", "Suspendido", "Renunciado", "Jubilado"], "command": lambda v: setattr(self.estado_doc_menu, '_current_value',v)}, 1, self, 'estado_doc_menu')
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
    