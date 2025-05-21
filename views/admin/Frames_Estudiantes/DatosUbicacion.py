import customtkinter as ctk
from util.widget_utils import *
from views.layouts.SectionFrameBase import SectionFrameBase
from .DatosPersonales import DatosPersonalesFrame

class DatosUbicacionFrame(SectionFrameBase):
    def __init__(self, master, vcmd_num): # vcmd_num se mantiene por si se añaden otros campos en el futuro
        super().__init__(master, header_text="Datos de Ubicación")
        self._crear_fila_widgets([
            ("Estado:", crear_entry, {"width":220}, 1, self, 'estado_entry'),
            ("Municipio:", crear_entry, {"width":220}, 1, self, 'municipio_entry')
        ])
        self._crear_fila_widgets([
            ("Parroquia:", crear_entry, {"width":220}, 1, self, 'parroquia_entry'),
            ("Sector:", crear_entry, {"width":220}, 1, self, 'sector_entry'),
            ("Calle:", crear_entry, {"width":220}, 1, self, 'calle_entry'),
            ("Nro Casa o Apartamento:", crear_entry, {"width":220}, 1, self, 'casa_apart_entry'),
            ("Tipo de Dirección:", crear_option_menu, {"values":["residencia", "trabajo",'otro'], "command": lambda v: setattr(self.tipo_direccion_menu, '_current_value',v)}, 1, self, 'tipo_direccion_menu', lambda w: w.set("residencia") )
        ])
        # CAMPOS DE TELÉFONO ELIMINADOS DE ESTA SECCIÓN

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
