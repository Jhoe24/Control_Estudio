import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class FrameNotaEstudiante(SectionFrameBase):
    def __init__(self, master, controller_estudiante, tupla):
        super().__init__(master, header_text="Gestión de Notas de Estudiantes")
        self.controller_estudiante = controller_estudiante
        self.lista_estudiantes = self.controller_estudiante.obtener_estudiantes_pnf(tupla)


        self.frames_estudiantes = []
        self.cargar_notas_estudiante()
            
        

    def cargar_notas_estudiante(self):
        """Crear frame por estudiante para cargar notas"""

        for idx, estudiante in enumerate(self.lista_estudiantes):
            frame = ctk.CTkFrame(self, fg_color="white", corner_radius=8)
            frame.pack(fill="x", padx=10, pady=5)

            # Grid horizontal para cada elemento
            frame.grid_columnconfigure(0, weight=0)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=0)
            frame.grid_columnconfigure(3, weight=0)
            frame.grid_columnconfigure(4, weight=0)

            # Labels
            label_documento = ctk.CTkLabel(frame, text=f"Documento: {estudiante['documento_identidad']}",font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
            label_documento.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

            label_nombre = ctk.CTkLabel(frame, text=f"Nombres: {estudiante['nombres']}",font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
            label_nombre.grid(row=0, column=1, padx=(20, 5), pady=10, sticky="w")

            label_nota = ctk.CTkLabel(frame, text="Ingrese Nota:",font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
            label_nota.grid(row=0, column=3, padx=5, pady=10, sticky="w")

            # Entry para nota
            entry_nota = ctk.CTkEntry(frame, width=80, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXTO_PRINCIPAL,font=FUENTE_LABEL_CAMPO)
            entry_nota.grid(row=0, column=4, padx=5, pady=10, sticky="w")

            btn_guardar = ctk.CTkButton(frame, width=150, text="Cargar Nota")
            btn_guardar.grid(row=0, column=5, padx=10, pady=10, sticky="w")

            


        #label = Documento    label = Nombre del estudiante    label = ingrese nota : entry    boton: cargar notas
