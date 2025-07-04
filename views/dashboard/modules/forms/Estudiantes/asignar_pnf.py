import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class AsignarPNFFrame(SectionFrameBase):
    def __init__(self, master, controller, controller_pnf, estudiante):
        super().__init__(master,"Asignar PNF a Estudiante")
        self.controller_pnf = controller_pnf
        self.estudiante = estudiante

       #mañana agrego los demas campos
    

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self.master, text="Asignar PNF", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.save_button = ctk.CTkButton(self.master, text="Guardar", command=self.save_data)
        self.save_button.pack(pady=10)

    def save_data(self):
        # Implement the logic to save the data
        pass