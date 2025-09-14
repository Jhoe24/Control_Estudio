import customtkinter as ctk
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.Carga_notas.form_nota_estudiante import FrameNotaEstudiante
from pprint import pprint

# UC   Profesor   Periodo Academico   Nota 
class ListadosEstudiantesNotas(ctk.CTkFrame):
    def __init__(self, master, controllers, user):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO)
        ctk.CTkLabel(self, text="Consulta de Notas", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).grid(row=0, column=0, pady= 0, padx=0, columnspan=6, sticky="ew")
        self.controller_user = controllers["Usuario"]
        self.controller_estudiantes = controllers["Estudiantes"]
        self.controller_notas = controllers["Notas"]
        persona_id = self.controller_user.obtener_persona_id(user)
        
        if persona_id:
            self.estudiante_id = self.controller_estudiantes.modelo.obtener_estudiante_id(persona_id)
            if self.estudiante_id:
                self.listado_notas = self.controller_notas.listarNotasEstudiante(self.estudiante_id)

                self.pagina_actual = 1
                self.uc_por_pagina = 11
                self.total_paginas = max(1, (len(self.listado_notas) + self.uc_por_pagina - 1) // self.uc_por_pagina)

                # lista de UC a mostrar en la página inicial
                self.paginas_mostrar = self.listado_notas[:self.uc_por_pagina]
                self.posicion_actual = len(self.paginas_mostrar)

                # variables para manejar botones dinámicos de cada fila
                self.button_uc = None
                self.frame_uc = None

                self.fila_datos = []

                headers = ["Unidad Curricular", "Trayecto", "Tramo", "Profesor", "Periodo Académico", "Nota"]
                for col, header in enumerate(headers):
                    # cada encabezado está dentro de un CTkFrame con fondo gris
                    celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
                    celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
                    label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color="#222")
                    label.pack(padx=10, pady=5)
                for i in range(len(headers)):
                    self.grid_columnconfigure(i, weight=1)


                # Frame de paginación
                self.frame_paginacion = ctk.CTkFrame(self, fg_color="transparent")
                self.frame_paginacion.grid_columnconfigure(0, weight=1)
                self.frame_paginacion.grid_columnconfigure(1, weight=0)
                self.frame_paginacion.grid_columnconfigure(2, weight=0)
                self.frame_paginacion.grid_columnconfigure(3, weight=0)
                self.frame_paginacion.grid_columnconfigure(4, weight=1)
                # mostrar o esconder paginación según cantidad de UC
                if len(self.listado_notas) <= self.uc_por_pagina:
                    self.frame_paginacion.grid_remove()
                else:
                    self.frame_paginacion.grid()
            
                # Botones de paginación
                self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", command=self.anterior_pagina)
                self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.total_paginas}", text_color="#222")
                self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina)

                self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
                self.label_pagina.grid(row=0, column=2, padx=5)
                self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

                # Coloca el frame de paginación al final de la tabla
                fila_paginacion = len(self.paginas_mostrar) + 2
                self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=6, pady=15, sticky="ew")

                if len(self.listado_notas) <= self.uc_por_pagina:
                    self.frame_paginacion.grid_remove()
                else:
                    self.frame_paginacion.grid()

                # Lista para almacenar las filas de datos
                self.mostrar_listado()
            else:
                ctk.CTkLabel(self, text="No es posible cargar las Notas", font=("Roboto", 16, "bold"), text_color=COLOR_BOTON_FONDO).pack(pady=(10, 20), padx=20, anchor="center")
        else:
            ctk.CTkLabel(self, text="No es posible cargar las Notas", font=("Roboto", 16, "bold"), text_color=COLOR_BOTON_FONDO).pack(pady=(10, 20), padx=20, anchor="center")
            
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
        #print(self.paginas_mostrar)
        for fila, dic_notas in enumerate(self.paginas_mostrar, start=2):
            fila_widgets = [
                self._crear_celda(fila, 0, dic_notas['unidad_curricular']),
                self._crear_celda(fila, 1, dic_notas['trayecto']),
                self._crear_celda(fila, 2, dic_notas['tramo']),
                self._crear_celda(fila, 3, dic_notas.get('nombre_docente') or "Editada por superior"),
                self._crear_celda(fila, 4, dic_notas['periodo_academico']),
                self._crear_celda(fila, 5, f"{dic_notas['valor']:.2f}"),
            ]
            self.fila_datos.append(fila_widgets)


    def anterior_pagina(self):
        """
            Retrocede a la página anterior de la tabla.
        """
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            nuevo_inicio = (self.pagina_actual - 1) * self.uc_por_pagina
            nuevo_fin = nuevo_inicio + self.uc_por_pagina
            self.paginas_mostrar = self.listado_notas[nuevo_inicio:nuevo_fin]
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
            self.paginas_mostrar = self.listado_notas[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")
            self.mostrar_listado()

        # Se actualiza la tabla

    def _crear_celda(self, row, col, texto):
        """
        Crea una celda de la tabla con el texto dado.
        """
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color="#222")
        label.pack(padx=10, pady=5)
        return celda
