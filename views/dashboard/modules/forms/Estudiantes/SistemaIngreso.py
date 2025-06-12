import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame


class SistemaIngresoFrame(SectionFrameBase):
    def __init__(self, master, vcmd_num):
        super().__init__(master, header_text="Sistema Nacional de Ingreso")
        self._crear_fila_widgets([
            ("Código:", crear_entry, {"width":150}, 1, self, 'codigo_entry'),
            ("Año:", crear_entry, {"width":100, "placeholder_text":"dd-mm-aaaa", "validate":"key", "validatecommand":(vcmd_num, "%S"), "placeholder_text":"aaaa"}, 1, self, 'anio_entry')
        ])
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def set_datos(self, estudiante):

        self.codigo_entry.delete(0, ctk.END)
        if estudiante.get('codigo_unico') != None and estudiante.get('codigo_unico') != "":
            self.codigo_entry.insert(0, estudiante.get("codigo_unico")) 
        self.codigo_entry.configure(state="disabled")   

        self.anio_entry.delete(0, 'end')
        self.anio_entry.insert(0, "0000")
        self.anio_entry.configure(state="disabled")

    #metodo para habilitar la edicion de los campos sin eliminar el contenido
    def habilitar_edicion(self):
        self.codigo_entry.configure(state="normal")
        self.anio_entry.configure(state="normal")