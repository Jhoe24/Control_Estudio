import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame

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

        # direccion_completa = estudiante.get("direccion_completa", "")
        # partes = [p.strip() for p in direccion_completa.split(',')]

        # estado = partes[0] if len(partes) > 0 else ""
        # municipio = partes[1] if len(partes) > 1 else ""
        # parroquia = partes[2] if len(partes) > 2 else ""
        # sector = partes[3] if len(partes) > 3 else ""
        # calle = partes[4] if len(partes) > 4 else ""
        # casa_apart = partes[5] if len(partes) > 5 else ""

        #configuaracion de estado
        self.estado_entry.delete(0,ctk.END)
        if estudiante.get("estado_direccion") != "" and estudiante.get("estado_direccion") != None:
            self.estado_entry.insert(0,estudiante.get("estado_direccion"))
        self.estado_entry.configure(state="disabled")

        self.municipio_entry.delete(0,ctk.END)
        if estudiante.get("municipio") != "" and estudiante.get("municipio") != None:
            self.municipio_entry.insert(0,estudiante.get("municipio"))
        self.municipio_entry.configure(state="disabled")

        self.parroquia_entry.delete(0,ctk.END)
        if estudiante.get("parroquia") != "" and estudiante.get("parroquia") != None:
            self.parroquia_entry.insert(0,estudiante.get("parroquia"))
        self.parroquia_entry.configure(state="disabled")

        self.sector_entry.delete(0,ctk.END)
        if estudiante.get("sector") != "" and estudiante.get("sector") != None:
            self.sector_entry.insert(0,estudiante.get("sector"))
        self.sector_entry.configure(state="disabled")
        
        self.calle_entry.delete(0,ctk.END)
        if estudiante.get("calle") != "" and estudiante.get("calle") != None:
            self.calle_entry.insert(0,estudiante.get("calle"))
        self.calle_entry.configure(state="disabled")

        self.casa_apart_entry.delete(0,ctk.END)
        if estudiante.get("casa_apart") != "" and estudiante.get("casa_apart") != None:
            self.casa_apart_entry.insert(0,estudiante.get("casa_apart"))
        self.casa_apart_entry.configure(state="disabled")

        if estudiante.get('tipo_direccion') != None and estudiante.get('tipo_direccion') != "":
            valor_tipo_direccion = estudiante.get("tipo_direccion")       
            self.var_opcion.set(valor_tipo_direccion)
        else:
            self.var_opcion.set("recidencia")
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

