import customtkinter as ctk

from views.dashboard.components import SectionFrameBase
from views.dashboard.components.widget_utils import create_option_menu_row


class ConfiguracionRespaldo(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.componentesVista()
     

    def componentesVista(self):
        #Componentes de impotacion y respaldo
        frameContenido = ctk.CTkFrame(self, fg_color="transparent")
        frameContenido.pack(pady=(40, 20), padx=20, fill="x", anchor="n")

        #Componentes de exportacion
        frameExportacion = ctk.CTkFrame(frameContenido, fg_color="transparent")
        frameExportacion.pack(pady=20)

        self.varTipoExpor = ctk.StringVar(value="*.xlxs")
        self.menuTipoExpor = create_option_menu_row(frameContenido, 
                                                    label_text="Seleccione el tipo de archivo",
                                                    options=  ["*.xlxs","*.db","csv"],
                                                    variable=self.varTipoExpor,
                                                    side_="left"
                                                    )
        ctk.CTkButton(
            frameExportacion,
            text="Realizar Exportacion",
        ).pack(side="left")