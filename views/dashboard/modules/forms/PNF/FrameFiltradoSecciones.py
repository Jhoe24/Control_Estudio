import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from controllers.dashboard.PNF.controller_pnf import ControllerPNF

from ..DatosPersonales import DatosPersonalesFrame

class FremeSecciones(SectionFrameBase):
    def __init__(self, master, controlador_pnf):
        super().__init__(master, "")
        self.controller_pnf = controlador_pnf   
      
        #Obterner datos pnf, trayecto y tramo
        self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
        self.var1 = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "") # Valor por defecto para el PNF
        
        self.tuple_pnf = self.controller_pnf.listado_pnf
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}  # nombre: id

      
        self._crear_fila_widgets([
            ("Seleccione un P.N.F:", crear_option_menu, {"values":self.nombres_pnf, "variable":self.var1, "command": self.set_trayecto  }, 1, self, 'pnf_menu'),
        ])

      #terminar el filtrado alinear bien el opion menu y colocar el boton
      