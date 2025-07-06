# views/admin/estudiante_form_view.py
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from views.dashboard.modules.forms.Carga_notas.cargar_notas import CargaNotasFrame



from views.dashboard.components.widget_utils import *


from config.app_config import AppConfig


class CargaNotasView(ctk.CTkScrollableFrame):

    def __init__(self, master, controlador_estudiante, controlador_pnf):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")

        self.datos_carga_notas = CargaNotasFrame(self,controlador_estudiante,controlador_pnf)

        