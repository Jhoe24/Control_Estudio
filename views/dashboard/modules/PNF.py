import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from views.dashboard.modules.forms.DatosUbicacion import DatosUbicacionFrame
from views.dashboard.modules.forms.PNF.FormPNF import DatosPNFPensumFrame
from views.dashboard.modules.forms.PNF.frameTrayecto import FrameTrayecto

from config.app_config import AppConfig

class FormularioPNFPensumView(ctk.CTkScrollableFrame):

    def __init__(self, master, controlador):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")
        self.master = master
        self.controlador = controlador
        self.datos_pnf = None
        self.datos_trayecto = None
        
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador._solo_decimal)
       
        self.datos_pnf = DatosPNFPensumFrame(self, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_trayecto = FrameTrayecto(self, self.vcmd_num_val, self.vcmd_fecha_val, self.vcmd_decimal_val)
        
        self.datos_trayecto.pack(fill="x", padx=10, pady=5)
        self.datos_pnf.pack(fill="x", padx=10, pady=5)
        
        