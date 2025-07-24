# views/admin/estudiante_form_view.py
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from views.dashboard.modules.forms.Carga_notas.cargar_notas import CargaNotasFrame
from views.dashboard.modules.tables.Carga_notas.Lis_estudiantes_pnf import ListadosEstudiantesPNF
from time import sleep 

from views.dashboard.components.widget_utils import *


from config.app_config import AppConfig


class CargaNotasView(ctk.CTkFrame):

    def __init__(self, master, controlador_estudiante, controlador_pnf, controller_secciones):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO)
        self.master = master
        self.controller_estudiantes = controlador_estudiante
        self.controller_pnf = controlador_pnf

        ctk.CTkLabel(self, text="Gestión de Carga de Notas", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        self.frame_contenedor_carga_notas = ctk.CTkFrame(self,
                                        fg_color="transparent",
                                        width=self.winfo_width(), 
                                        height=350)
        self.frame_contenedor_carga_notas.pack(fill="x", pady=10)
        

        self.datos_carga_notas = CargaNotasFrame(self.frame_contenedor_carga_notas, controlador_estudiante, controlador_pnf, controller_secciones)
        self.datos_carga_notas.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para los botones
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=10)


        self.btn_siguiente = ctk.CTkButton(
            self.btn_frame, 
            text="Siguiente", width=150,
            height=40,
            text_color="#ffffff",
            fg_color=COLOR_BOTON_FONDO,
            hover_color=COLOR_BOTON_FONDO_HOVER,
            command=self.mostrar_listado
        )
        self.btn_siguiente.pack(side="top", padx=(0, 4), pady=5)

        self.btn_volver = ctk.CTkButton(
            self, text="Volver", width=100,
            text_color="#ffffff",
            fg_color=COLOR_BOTON_FONDO,
            hover_color=COLOR_BOTON_FONDO_HOVER,
           # command=self.mostrar_listado
        )

    def mostrar_listado(self):
        self.btn_siguiente.grid_remove()
        tuplas_datos = self.datos_carga_notas.obtener_filtros_seleccionados()
        self.frame_contenedor_carga_notas.destroy()
        self.btn_siguiente.destroy()
        
        listado_instancia = ListadosEstudiantesPNF(self,self.controller_estudiantes,self.controller_pnf, tuplas_datos)
        listado_instancia.pack(fill="both", expand=True, padx=10, pady=10)

        
        self.btn_siguiente = ctk.CTkButton(
            self, text="Siguiente", 
            width=150,
            height=40,
            text_color="#ffffff",
            fg_color=COLOR_BOTON_FONDO,
            hover_color=COLOR_BOTON_FONDO_HOVER,
            command=self.next
        )
        self.btn_siguiente.pack(side="right", padx=(0, 4), pady=5)
        self.btn_volver.pack(side="left", padx=(0, 4), pady=5)


    def next(self):pass

        