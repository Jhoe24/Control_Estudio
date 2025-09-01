import customtkinter as ctk
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.tables.PNF.ListarUC import ListarUC
from views.dashboard.modules.forms.Carga_notas.form_nota_estudiante import FrameNotaEstudiante
from pprint import pprint

class ListadosEstudiantesPNF(ListarUC):
    def __init__(self, master,controlladores,tuplas_datos, user = None, rol = None):
        super().__init__(master=master,controller=controlladores,tupla_datos=tuplas_datos,username=user,user_role=rol)

        self.controller_estudiante = controlladores["Periodos"]
        self.controller_estudiantes_inscritos = controlladores["Estudiantes"]

        self.user_role

        self.tuplas_datos = tuplas_datos
        
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
        for fila, dic_uc in enumerate(self.paginas_mostrar, start=2):
            fila_widgets = [
                self._crear_celda(fila, 0, dic_uc['codigo']),
                self._crear_celda(fila, 1, dic_uc['nombre']),
                self._crear_celda(fila, 2, dic_uc['trayecto_id']),
                self._crear_celda(fila, 3, dic_uc['tramo_id']),
            ]
            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=6)
            celda_btn.grid(row=fila, column=4, padx=1, pady=6, sticky="nsew")

            # Frame interno para centrar los botones
            frame_botones = ctk.CTkFrame(celda_btn, fg_color="transparent")
            frame_botones.pack(expand=True)

            if self.user_role and self.user_role.lower()== "estudiante":
                    print("simon")
            else:
                button = ctk.CTkButton(
                    frame_botones,
                    text="Gestionar Notas",
                    width=100,
                    text_color="#ffffff",
                    fg_color=COLOR_BOTON_FONDO,
                    hover_color=COLOR_BOTON_FONDO_HOVER,
                    command=lambda uc_id = dic_uc["id"]: self.cargar_nota_uc(uc_id)
                )

            # button_ver_notas = ctk.CTkButton(
            #     frame_botones, text="Ver Notas", width=100,
            #     text_color="#ffffff",
            #     fg_color=COLOR_BOTON_FONDO,
            #     hover_color=COLOR_BOTON_FONDO_HOVER,
            #     command=lambda uc_id = dic_uc["id"]: self.ver_notas_uc(uc_id)
            # )
                button.pack(side="left", padx=(0,4), pady=5)
            #button_ver_notas.pack(side="left", pady=5)

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

    def cargar_nota_uc(self, unidad_curricular_id):
        """
            Crear una ventana modal para mostrar los datos.
        """
        top = ctk.CTkToplevel(self, fg_color="White")
        top.title("Notas de la Unidad Curricular")
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
        # Configurar el layout de la ventana modal para que el contenido principal se expanda
        # La primera fila (donde estará el scroll_frame) debe expandirse
        top.grid_rowconfigure(0, weight=1)
        # La segunda fila (donde estará el botón) no se expandirá
        top.grid_rowconfigure(1, weight=0)
        # La única columna se expandirá para centrar el contenido
        top.grid_columnconfigure(0, weight=1)

        # Scroll principal del modal
        scroll_frame = ctk.CTkScrollableFrame(top, fg_color="White")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0)) # pady(top, bottom)

        
        #print(unidad_curricular_id)
        carga_noras_estudiantes = FrameNotaEstudiante(
            scroll_frame,
            self.controller_estudiantes_inscritos,
            self.tuplas_datos,
            unidad_curricular_id,
            solo_lectura=False,
            user_role=self.user_role
        )
        carga_noras_estudiantes.pack(fill="x", padx=10, pady=10)

        btn_cerrar = ctk.CTkButton(
            top,
            fg_color=COLOR_BOTON_FONDO,
            hover_color=COLOR_BOTON_FONDO_HOVER,
            text="Cerrar",
            width=150,
            height=40,
            command=top.destroy
        )
        btn_cerrar.grid(row=1, column=0, pady=(10, 20), sticky="s")

    def ver_notas_uc(self, unidad_curricular_id):
        """
        Crear una ventana modal para mostrar las notas de los estudiantes en modo solo lectura.
        """
        top = ctk.CTkToplevel(self, fg_color="White")
        top.title("Ver Notas de la Unidad Curricular")
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
    
        notas_estudiantes = FrameNotaEstudiante(
            scroll_frame,
            self.controller_estudiantes_inscritos,
            self.tuplas_datos,
            unidad_curricular_id,
            solo_lectura=True
        )
        notas_estudiantes.pack(fill="x", padx=10, pady=10)

