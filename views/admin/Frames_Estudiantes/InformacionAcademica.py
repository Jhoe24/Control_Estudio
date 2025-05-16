import customtkinter as ctk
from util.widget_utils import *
from views.layouts.SectionFrameBase import SectionFrameBase
from .DatosPersonales import DatosPersonalesFrame

class InformacionAcademicaFrame(SectionFrameBase):
    def __init__(self, master, vcmd_fecha, vcmd_decimal):
        super().__init__(master, header_text="Información Académica")
        self._crear_fila_widgets([
            ("Mención:", crear_option_menu, {"values":["Profesional", "Técnico Superior Universitario", "Bachiller"], "command": lambda v: setattr(self.tipo_inst_menu, '_current_value',v)}, 1, self, 'tipo_inst_menu', lambda w: w.set("Bachiller")),
            ("Tipo Institución:", crear_option_menu, {"values":["Pública", "Privada"], "command": lambda v: setattr(self.tipo_inst_menu, '_current_value',v)}, 1, self, 'tipo_inst_menu', lambda w: w.set("Pública"))
        ])
        self._crear_fila_widgets([
            ("Institución:", crear_entry, {"width":250}, 2, self, 'institucion_entry'),
            ("Fecha Grado:", crear_entry, {"width":120, "validate":"key", "validatecommand":(vcmd_fecha, "%S"), "placeholder_text":"dd/mm/aaaa"}, 1, self, 'fgrado_entry'),
            ("Promedio Bachillerato:", crear_entry, {
                "width":120,
                "validate":"key",
                "validatecommand":(vcmd_decimal, "%P", "%S")
            }, 1, self, 'promedio_entry')
        ])
        self._crear_fila_widgets([
            ("Título Obtenido:", crear_entry, {"width":220}, 2, self, 'titulo_entry')
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
