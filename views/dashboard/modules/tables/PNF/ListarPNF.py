import customtkinter as ctk
import tkinter as tk
import threading
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.PNF.FormPNF import DatosPNFPensumFrame

class ListarPNF(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="white")
        self.controller = controller
        self.lista_pnf = self.controller.listado_pnf  # Debe ser una lista de tuplas (id, codigo, nombre)
        
        self.cantidad_mostrar = 10

        self.cantidad_paginas = (len(self.lista_pnf) // self.cantidad_mostrar) + (1 if len(self.lista_pnf) % self.cantidad_mostrar > 0 else 0)

        self.filas_datos = []
        """
        Implementar logica para la paginacion 
        """
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controller._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controller._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controller._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controller._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controller._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controller._solo_decimal)


        # --- ENCABEZADOS (FILA 1) ---
        headers = ["ID", "Código", "Nombre", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color="#222")
            label.pack(padx=10, pady=5)
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)


      
# --- PAGINACIÓN (se ubicará dinámicamente al final de los datos) ---
        self.frame_paginacion = ctk.CTkFrame(self, fg_color="transparent")

        # Configuración de columnas para centrar los elementos de paginación
        self.frame_paginacion.grid_columnconfigure(0, weight=1)
        self.frame_paginacion.grid_columnconfigure(1, weight=0)
        self.frame_paginacion.grid_columnconfigure(2, weight=0)
        self.frame_paginacion.grid_columnconfigure(3, weight=0)
        self.frame_paginacion.grid_columnconfigure(4, weight=1)

        self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", state="disabled")
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text="1 de 1", text_color="#222")
        self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente", state="disabled")

        self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
        self.label_pagina.grid(row=0, column=2, padx=5)
        self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

        # Coloca el frame de paginación al final de la tabla (ajusta la fila según tus datos)
        fila_paginacion = len(self.lista_pnf) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=4, pady=15, sticky="ew")
                
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
        dic_datos = self.controller.obtener_datos_completos(pnf[0])
        top = ctk.CTkToplevel(self,fg_color="White")
        ancho = 900
        alto = 700

        # Obtén el tamaño de la pantalla
        top.update_idletasks()  # Asegura que winfo_screenwidth/height sean correctos
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()

        # Calcula la posición centrada
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)

        top.geometry(f"{ancho}x{alto}+{x}+{y}")
        top.lift()
        top.focus_force()
        top.grab_set()

        #agregar scroll
        scroll_frame = ctk.CTkScrollableFrame(top,fg_color="White")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        frame_pnf = DatosPNFPensumFrame(scroll_frame,self.vcmd_num_val,self.vcmd_fecha_val)
        frame_pnf.set_datos(dic_datos)
        frame_pnf.pack(fill="x", padx=20, pady=10)


