import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *

class FiltradoSecciones(ctk.CTkFrame):
    def __init__(self, master, controlador_pnf, controlador_secciones):
        super().__init__(master,fg_color="white")
        self.controller_pnf = controlador_pnf   
        self.controller_secciones = controlador_secciones
        self.master = master
        
        #Obterner datos pnf, trayecto y tramo
        self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
        self.var1 = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "") # Valor por defecto para el PNF
        
        self.tuple_pnf = self.controller_pnf.listado_pnf
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}  # nombre: id

        frame = ctk.CTkFrame(self,fg_color="transparent")
        frame.pack(pady=PADY_FILA, padx=15, side = "left")

        self.pnf_menu = crear_option_menu(
            frame,
            values=self.nombres_pnf,
            variable=self.var1,
            #command=self.set_trayecto
        )

        self.btn_buscar = ctk.CTkButton(
            frame,
            text="Buscar",
            font=FUENTE_BOTON, 
            hover_color=COLOR_BOTON_PRIMARIO_HOVER, 
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.realizar_busquedad
        )

        self.pnf_menu.pack(side="left", padx=(0, 15))
        self.btn_buscar.pack(side="left", padx=(20, 15))
        
    def obtener_pnf_id(self):
        nombre_seleccionado = self.var1.get()
        if nombre_seleccionado in self.pnf_id_por_nombre:
            return self.pnf_id_por_nombre[nombre_seleccionado]
        else:
            return None
    
    def realizar_busquedad(self):
        pnf_id = self.obtener_pnf_id()
      
        #self.master.secciones = self.controller_secciones.listar_secciones(pnf_id)
        #print("dddd",len(self.master.secciones))
        self.master.actualizar_listado(pnf_id)
        print("probando")
        #self.master.calcular_pagina()

    def actualizar_listado_por_busqueda(self,pnf_id):
        self.realizar_busquedad(pnf_id)