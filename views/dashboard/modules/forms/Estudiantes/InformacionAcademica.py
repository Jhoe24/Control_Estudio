import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class InformacionAcademicaFrame(SectionFrameBase):
    def __init__(self, master, vcmd_fecha, vcmd_decimal):
        super().__init__(master, header_text="Información Académica")
        self.var_condicion = ctk.StringVar(value='Regular')
        self._crear_fila_widgets([
            ("Mención:", crear_option_menu, {"values":["Profesional", "Técnico Superior Universitario", "Bachiller"], "command": lambda v: setattr(self.tipo_mencion_menu, '_current_value',v)}, 1, self, 'tipo_mencion_menu', lambda w: w.set("Bachiller")),
            ("Tipo Institución:", crear_option_menu, {"values":["Pública", "Privada"], "command": lambda v: setattr(self.tipo_inst_menu, '_current_value',v)}, 1, self, 'tipo_inst_menu', lambda w: w.set("Pública"))
        ])
        self._crear_fila_widgets([
            ("Institución:", crear_entry, {"width":300}, 1, self, 'institucion_entry'),
            ("Fecha Grado:", crear_entry, {"width":120, "placeholder_text":"dd-mm-aaaa", "validate":"key", "validatecommand":(vcmd_fecha, "%S"), "placeholder_text":"dd-mm-aaaa"}, 1, self, 'fgrado_entry'),
            ("Promedio Bachillerato:", crear_entry, {
                "width":120,
                "validate":"key",
                "validatecommand":(vcmd_decimal, "%P", "%S")
            }, 1, self, 'promedio_entry')
        ])
        self._crear_fila_widgets([
            ("Título Obtenido:", crear_entry, {"width":300}, 1, self, 'titulo_entry')
        ])
        self._crear_fila_widgets([
            ("Condición:", crear_option_menu, {"values":["Regular", "Repitente", "Reingreso", "Transferencia"],"variable":self.var_condicion, "command": lambda v: setattr(self.condicion_menu, '_current_value',v)}, 1, self, 'condicion_menu')
        ])
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def set_datos(self, estudiante):
        # Asignar valores y deshabilitar campos
        self.tipo_mencion_menu.set("Bachiller")
        self.tipo_mencion_menu.configure(state="disabled")

        self.tipo_inst_menu.set(("Pública"))
        self.tipo_inst_menu.configure(state="disabled")

        self.institucion_entry.delete(0, ctk.END)
        if estudiante.get('institucion_procedencia') != None and estudiante.get('institucion_procedencia') != "":
            self.institucion_entry.insert(0, estudiante.get("institucion_procedencia")) 
        self.institucion_entry.configure(state="disabled")

        #Configuracion fecha de grado
        self.fgrado_entry.delete(0, ctk.END)
        if estudiante.get('fecha_grado_bachiller') != None and estudiante.get('fecha_grado_bachiller') != "":
            self.fgrado_entry.insert(0, estudiante.get("fecha_grado_bachiller")) 
        self.fgrado_entry.configure(state="disabled")

        #Configuaracion de promedio
        self.promedio_entry.delete(0, ctk.END)
        self.promedio_entry.insert(0,"000")
        self.promedio_entry.configure(state="disabled")

        self.titulo_entry.delete(0, ctk.END)
        if estudiante.get('mencion_bachiller') != None and estudiante.get('mencion_bachiller') != "":
            self.titulo_entry.insert(0, estudiante.get("mencion_bachiller")) 
        self.titulo_entry.configure(state="disabled")

        if estudiante.get('condicion'):
            self.var_condicion.set(estudiante.get('condicion'))
        else:
            self.var_condicion.set('Regular')
        self.condicion_menu.configure(state="disabled")

    #metodo para habilitar la edicion de los campos sin eliminar el contenido
    def habilitar_edicion(self):
        self.tipo_mencion_menu.configure(state="normal")
        self.tipo_inst_menu.configure(state="normal")
        self.institucion_entry.configure(state="normal")
        self.fgrado_entry.configure(state="normal")
        self.promedio_entry.configure(state="normal")
        self.titulo_entry.configure(state="normal")
        self.condicion_menu.configure(state="normal")
    