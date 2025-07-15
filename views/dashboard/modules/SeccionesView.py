import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.PNF.FrameSecciones import FremeSecciones


class SeccionView(ctk.CTkScrollableFrame):
    def __init__(self, master, controller_Doc, controller_pnf):
        super().__init__(master, fg_color="transparent")
        self.controller_Doc = controller_Doc
        self.controller_pnf = controller_pnf
        self.form_seccion = FremeSecciones(self, self.controller_Doc, self.controller_pnf)
        