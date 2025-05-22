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
        self.var_opcion = ctk.StringVar(value='residencia')
        self._crear_fila_widgets([
            ("Parroquia:", crear_entry, {"width":220}, 1, self, 'parroquia_entry'),
            ("Sector:", crear_entry, {"width":220}, 1, self, 'sector_entry'),
            ("Calle:", crear_entry, {"width":220}, 1, self, 'calle_entry'),
            ("Nro Casa o Apartamento:", crear_entry, {"width":220}, 1, self, 'casa_apart_entry'),
            ("Tipo de Dirección:", crear_option_menu, {"values":["residencia", "trabajo",'otro'], "variable":self.var_opcion, "command": lambda v: setattr(self.tipo_direccion_menu, '_current_value',v)}, 1, self, 'tipo_direccion_menu')
        ])
        # CAMPOS DE TELÉFONO ELIMINADOS DE ESTA SECCIÓN

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def set_datos(self, estudiante):

        direccion_completa = estudiante.get("direccion_completa", "")
        partes = [p.strip() for p in direccion_completa.split(',')]

        estado = partes[0] if len(partes) > 0 else ""
        municipio = partes[1] if len(partes) > 1 else ""
        parroquia = partes[2] if len(partes) > 2 else ""
        sector = partes[3] if len(partes) > 3 else ""
        calle = partes[4] if len(partes) > 4 else ""
        casa_apart = partes[5] if len(partes) > 5 else ""


        self.estado_entry.configure(state="normal")
        self.estado_entry.delete(0, 'end')
        self.estado_entry.insert(0, estado)
        self.estado_entry.configure(state="disabled")

        self.municipio_entry.configure(state="normal")
        self.municipio_entry.delete(0, 'end')
        self.municipio_entry.insert(0, municipio)
        self.municipio_entry.configure(state="disabled")

        self.parroquia_entry.configure(state="normal")
        self.parroquia_entry.delete(0, 'end')
        self.parroquia_entry.insert(0, parroquia)
        self.parroquia_entry.configure(state="disabled")
        
        self.sector_entry.configure(state="normal")
        self.sector_entry.delete(0, 'end')
        self.sector_entry.insert(0, sector)
        self.sector_entry.configure(state="disabled")

        self.calle_entry.configure(state="normal")
        self.calle_entry.delete(0, 'end')
        self.calle_entry.insert(0, calle)
        self.calle_entry.configure(state="disabled")

        self.casa_apart_entry.configure(state="normal")
        self.casa_apart_entry.delete(0, 'end')
        self.casa_apart_entry.insert(0, casa_apart)
        self.casa_apart_entry.configure(state="disabled")

        valor_tipo_direccion = estudiante.get("tipo_direccion")
        print(f"Valor de tipo_direccion: {valor_tipo_direccion}")
        self.var_opcion.set(valor_tipo_direccion)
        self.tipo_direccion_menu.configure(state="disabled")

    #metodo para habilitar la edicion de los campos sin eliminar el contenido
    def habilitar_edicion(self):
        self.estado_entry.configure(state="normal")
        self.municipio_entry.configure(state="normal")
        self.parroquia_entry.configure(state="normal")
        self.sector_entry.configure(state="normal")
        self.calle_entry.configure(state="normal")
        self.casa_apart_entry.configure(state="normal")
        self.tipo_direccion_menu.configure(state="normal")

