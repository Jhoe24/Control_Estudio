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
    def __init__(self, master, controladores, user = None, rol = None):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO)
        self.master = master
        self.controller_estudiantes = controladores["Periodos"]
        self.controller_pnf = controladores["PNF"]
        self.controller_estudiantes_inscritos = controladores["Estudiantes"]
        self.controladores = controladores
        self.user = user
        self.rol = rol
        self.docente_id = None
        if user:
            persona_id = self.controladores["Usuario"].obtener_persona_id(self.user)
            self.docente_id = self.controladores["Docentes"].obtener_id_docente(persona_id)

        self.titulo = ctk.CTkLabel(self, text="Gestión de Carga de Notas", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL)
        self.titulo.pack(pady=(10, 20), padx=20, anchor="w")

        self.frame_contenedor_carga_notas = ctk.CTkFrame(self,
                                        fg_color="transparent",
                                        width=self.winfo_width(), 
                                        height=350)
        self.frame_contenedor_carga_notas.pack(fill="x", pady=10)
        

        # El orden correcto es: master, controller_periodos_academicos, controller_pnf, controller_secciones
        self.datos_carga_notas = CargaNotasFrame(self.frame_contenedor_carga_notas, self.controller_estudiantes, self.controller_pnf, controladores["Secciones"],docente_id=self.docente_id, rol=self.rol)
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

        # self.btn_volver = ctk.CTkButton(
        #     self, text="Volver", width=100,
        #     text_color="#ffffff",
        #     fg_color=COLOR_BOTON_FONDO,
        #     hover_color=COLOR_BOTON_FONDO_HOVER,
        #    # command=self.mostrar_listado
        # )

    def mostrar_listado(self):
        tuplas_datos = self.datos_carga_notas.obtener_filtros_seleccionados()
      
        self.datos_carga_notas.destroy()
        self.btn_frame.destroy()
        self.frame_contenedor_carga_notas.destroy()  # <-- destruye el contenedor

        # Crea un nuevo contenedor para el listado
        self.frame_contenedor_carga_notas = ctk.CTkFrame(self,
                                        fg_color="transparent",
                                        width=self.winfo_width(), 
                                        height=350)
        self.frame_contenedor_carga_notas.pack(fill="x", pady=10)
        if self.rol and self.rol.lower() not in ["docente", "coord_pnf"]:
            self.titulo.configure(text = f"Gestión de Carga de Notas de {tuplas_datos[3]} {tuplas_datos[4]}")
            
        listado_instancia = ListadosEstudiantesPNF(self.frame_contenedor_carga_notas,self.controladores,tuplas_datos,user = self.user, rol = self.rol)
        listado_instancia.pack(fill="both", expand=True, padx=10, pady=10)
        
        # self.btn_siguiente = ctk.CTkButton(
        #     self, text="Siguiente", 
        #     width=150,
        #     height=40,
        #     text_color="#ffffff",
        #     fg_color=COLOR_BOTON_FONDO,
        #     hover_color=COLOR_BOTON_FONDO_HOVER,
        #     command=self.next
        # )
        # self.btn_siguiente.pack(side="right", padx=(0, 4), pady=5)
        #self.btn_volver.pack(side="left", padx=(0, 4), pady=5)


    def next(self):pass
