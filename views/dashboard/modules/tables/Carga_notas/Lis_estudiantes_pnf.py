import customtkinter as ctk
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.tables.PNF.ListarUC import ListarUC
from views.dashboard.modules.forms.Carga_notas.form_nota_estudiante import FrameNotaEstudiante


class ListadosEstudiantesPNF(ListarUC):
    def __init__(self, master,controller_estudinates, controller_pnf,tuplas_datos):
        super().__init__(master=master,controller=controller_pnf,tupla_datos=tuplas_datos)
        self.controller_estudiante = controller_estudinates
        

    def mostrar_listado(self):
        """
        Muestra la lista de UC en la tabla sin tener nada que ver con el filtrado 
        y recibiendo los datos de un diccionario
        """
        # Se limpia la tabla
        for fila in self.fila_datos:
            for widget in fila:
                widget.destroy()
        self.fila_datos.clear()
        
        self.fila_datos = []
        # se obtienen los datos y me devuelve el diccionario
        for fila, dic_uc in enumerate(self.paginas_mostrar, start=2):
            fila_widgets = [
                self._crear_celda(fila, 0, dic_uc['codigo']),
                self._crear_celda(fila, 1, dic_uc['nombre']),
                self._crear_celda(fila, 2, dic_uc['horas_totales']),
                self._crear_celda(fila, 3, dic_uc['unidades_credito']),
            ]
            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=fila, column=4, padx=1, pady=1, sticky="nsew")
            button = ctk.CTkButton(
                celda_btn,
                text="Cargar Notas",
                width=120,
                text_color="#222",
                command=lambda: self.cargar_nota_uc(dic_uc)
            )
            button.pack(padx=10, pady=5)
            fila_widgets.append(celda_btn)
            self.fila_datos.append(fila_widgets)
            
    
    def anterior_pagina(self):
        """
        Retrocede a la página anterior de la tabla.
        """
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            nuevo_inicio = (self.pagina_actual - 1) * self.uc_por_pagina
            nuevo_fin = nuevo_inicio + self.uc_por_pagina
            self.paginas_mostrar = self.lista_UC[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")
            self.mostrar_listado()
        
    def siguiente_pagina(self):
        """
        Avanza a la siguiente página de la tabla.
        """
        nuevo_inicio = self.pagina_actual * self.uc_por_pagina
        nuevo_fin = nuevo_inicio + self.uc_por_pagina
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.paginas_mostrar = self.lista_UC[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")
            self.mostrar_listado()

        # Se actualiza la tabla

    def cargar_nota_uc(self, dic_uc):
        """
        Crear una ventana modal para mostrar los datos.
        """
        top = ctk.CTkToplevel(self, fg_color="White")
        top.title("Datos Completos del PNF")
        ancho = 1000
        alto = 700

        # Centrar ventana
        top.update_idletasks()
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width // 2) - (ancho // 2) + 100
        y = (screen_height // 2) - (alto // 2)
        top.geometry(f"{ancho}x{alto}+{x}+{y}")
        top.lift()
        top.focus_force()
        top.grab_set()

        # Scroll principal del modal
        scroll_frame = ctk.CTkScrollableFrame(top, fg_color="White")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        carga_noras_estudiantes = FrameNotaEstudiante(scroll_frame,self.controller_estudiante,self.tuplas_nombre)
        carga_noras_estudiantes.pack(fill = "x", padx = 10, pady = 10)
        
