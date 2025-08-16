import customtkinter as ctk
import tkinter as tk
from views.dashboard.components.widget_utils import *


class FrameRoles(ctk.CTkFrame):
    def __init__(self, master, controller, datos_usuario):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.controler = controller
        self.datos_usuario = datos_usuario


