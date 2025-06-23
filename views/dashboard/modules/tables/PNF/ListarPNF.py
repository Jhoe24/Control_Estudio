import customtkinter as ctk
import tkinter as tk
import threading
from views.dashboard.components.widget_utils import *

class ListarPNF(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="white")
        self.controller = controller
        self.lista_pnf = self.controller.listado_pnf  # Debe ser una lista de tuplas (id, codigo, nombre)
        self.filas_datos = []

        # --- ENCABEZADOS (FILA 1) ---
        headers = ["ID", "Código", "Nombre", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color="#222")
            label.pack(padx=10, pady=5)
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)

        self.mostrar_listado()

    def mostrar_listado(self):
        # Empieza en la fila 2 porque la fila 1 es el encabezado
        for fila, tupla_pnf in enumerate(self.lista_pnf, start=2):
            fila_widgets = [
                self._crear_celda(fila, 0, tupla_pnf[0]),  # ID
                self._crear_celda(fila, 1, tupla_pnf[1]),  # Código
                self._crear_celda(fila, 2, tupla_pnf[2]),  # Nombre
            ]
            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=fila, column=3, padx=1, pady=1, sticky="nsew")
            boton = ctk.CTkButton(
                celda_btn, text="Ver datos", width=100,
                text_color="#222",
                command=lambda pnf=tupla_pnf: self.ver_datos_completos(pnf)
            )
            boton.pack(padx=10, pady=5)
            fila_widgets.append(celda_btn)
            self.filas_datos.append(fila_widgets)

    def _crear_celda(self, row, col, texto):
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color="#222")
        label.pack(padx=10, pady=5)
        return celda

    def ver_datos_completos(self, pnf):
        # Por ahora no hace nada, puedes implementar la lógica aquí más adelante
        pass