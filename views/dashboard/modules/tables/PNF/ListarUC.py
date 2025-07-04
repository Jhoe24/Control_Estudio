import customtkinter as ctk
import tkinter as tk
from views.dashboard.components.widget_utils import *


class ListarUC(ctk.CTkScrollableFrame):

    def __init__(self, master, controller):
        super().__init__(master, fg_color="white")
        self.controller = controller
        self.lista_UC = self.controller.obtener_UC()

        self.pagina_actual = 1
        self.uc_por_pagina = 10
        self.total_paginas = (len(self.lista_UC) + self.uc_por_pagina - 1) // self.uc_por_pagina

        self.paginas_mostrar = self.lista_UC[:self.uc_por_pagina]
        self.posicion_actual = len(self.paginas_mostrar)

        self.fila_datos = []

        # Encabezados de la tabla
        headers = ["Código", "Nombre", "Credito","Horas", "Acciones"]
        for col, header in enumerate(headers):
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

        self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", command=self.anterior_pagina)
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.total_paginas}", text_color="#222")
        self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina)

        self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
        self.label_pagina.grid(row=0, column=2, padx=5)
        self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

        # Coloca el frame de paginación al final de la tabla
        fila_paginacion = len(self.paginas_mostrar) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=4, pady=15, sticky="ew")

        # Lista para almacenar las filas de datos
        self.mostrar_listado()
        
    def mostrar_listado(self):
        """
        Muestra la lista de UC en la tabla, con sus botones de acción.
        """
        # Limpia las filas anteriores
        for fila in self.fila_datos:
            for widget in fila:
                widget.destroy()
        self.fila_datos.clear()
        # Empieza en la fila 2 porque la fila 1 es el encabezado
        for fila, tupla_uc in enumerate(self.paginas_mostrar, start=2):
            fila_widgets = [
                self._crear_celda(fila, 0, tupla_uc[0]),  # Código
                self._crear_celda(fila, 1, tupla_uc[1]),  # Nombre
                self._crear_celda(fila, 2, tupla_uc[2]),  # Crédito
                self._crear_celda(fila, 3, tupla_uc[3]),  # Horas
            ]
            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=fila, column=4, padx=1, pady=1, sticky="nsew")
            boton = ctk.CTkButton(
                celda_btn, text="Ver datos", width=100,
                text_color="#222",
                command=lambda uc=tupla_uc: self.ver_datos_completos(uc)
            )
            boton.pack(padx=10, pady=5)
            fila_widgets.append(celda_btn)
            self.fila_datos.append(fila_widgets)


    def _crear_celda(self, row, col, texto):
        """
        Crea una celda de la tabla con el texto dado.
        """
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color="#222")
        label.pack(padx=10, pady=5)
        return celda
    
    def anterior_pagina(self):
        pass
    def siguiente_pagina(self):
        pass
    
