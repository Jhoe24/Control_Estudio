import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

from ..DatosPersonales import DatosPersonalesFrame

class DatosPNFPensumFrame(SectionFrameBase):
    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, header_text="Datos de PNF y Pensum")
        