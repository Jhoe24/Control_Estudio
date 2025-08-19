import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
import tkinter.messagebox as messagebox
import tkinter as tk

class FiltradoPNFFrame(SectionFrameBase):
    def __init__(self, master, controllers, user_role=None, username=None):
        super().__init__(master, header_text="Filtrar Unidades Curriculares por PNF")
        self.master = master
        self.user_role = user_role
        self.username = username
        self.controlador = controllers
        # self.controlador_docente = controllers['Docentes']
        # self.controlador_user = controllers['Usuario']

         # --- Lista de PNF del controlador ---
        self.lista_pnf = self.controlador.listado_pnf  # lista de tuplas (id_pnf, nombre_pnf, nombre_pnf)
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.lista_pnf}

        # Inicializar variables
        pnf_coordinador = None
        self.valores_pnf = self.obtener_nombre_pnf() or ["Sin opciones disponibles"]
        valor_inicial = self.valores_pnf[0]

        # Configurar valores para coordinador
        if user_role and user_role.lower() == "coord_pnf" and username:
            try:
                persona_id = self.controlador_user.obtener_persona_id(username)
                docente_id = self.controlador_docente.obtener_id_docente(persona_id)
                pnf_id = self.controlador_docente.obtener_pnf_id(docente_id)
                
                if pnf_id:
                    pnf_coordinador = next(
                        (nombre for nombre, id_ in self.pnf_id_por_nombre.items() if id_ == pnf_id),
                        None
                    )
                    
                    if pnf_coordinador:
                        self.valores_pnf = [pnf_coordinador]
                        valor_inicial = pnf_coordinador
                    else:
                        self.valores_pnf = ["Sin opciones disponibles"]
                        valor_inicial = "Sin opciones disponibles"
            except Exception as e:
                print(f"Error obteniendo PNF del coordinador: {e}")
                self.valores_pnf = ["Error al cargar PNF"]
                valor_inicial = "Error al cargar PNF"


        self.pnf_var = ctk.StringVar(value=valor_inicial)
        self.trayecto_var = ctk.StringVar(value="No seleccionado")
        self.tramo_var = ctk.StringVar(value="No seleccionado")

        self.frame_filtro_pnf = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtro_pnf.pack(fill="x", pady=PADY_FILA, padx=15)

        
            

        # --- OptionMenu PNF ---
        self.option_menu_pnf = crear_option_menu(
            self.frame_filtro_pnf,
            values=self.valores_pnf,
            variable=self.pnf_var,
            width=300,
            command=self.actualizar_trayectos_por_pnf
        )

        # if nombre_pnf:
        #     self.pnf_var.set(nombre_pnf)
        #     self.option_menu_pnf.configure(state="disabled")

        self.option_menu_pnf.pack(side="left", padx=(0, 15))

        # Bloquear PNF si es coordinador
        if user_role and user_role.lower() == "coord_pnf" and pnf_coordinador:
            self.option_menu_pnf.configure(state="disabled")
            # Ejecutar búsqueda automáticamente para coordinador
            self.ejecutar_busqueda()

        # --- OptionMenu Trayecto ---
        self.option_menu_trayecto = crear_option_menu(
            self.frame_filtro_pnf,
            values=["No seleccionado"],
            variable=self.trayecto_var,
            width=200,
            command=self.actualizar_tramos_por_trayecto
        )
        self.option_menu_trayecto.pack(side="left", padx=(0, 15))

        # --- OptionMenu Tramo ---
        self.option_menu_tramo = crear_option_menu(
            self.frame_filtro_pnf,
            values=["No seleccionado"],
            variable=self.tramo_var,
            width=200
        )
        self.option_menu_tramo.pack(side="left", padx=(0, 15))

        # --- Botón de búsqueda ---
        self.boton_buscar = ctk.CTkButton(
            self.frame_filtro_pnf,
            text="Buscar",
            command=self.ejecutar_busqueda
        )
        self.boton_buscar.pack(side="left")

    def actualizar_trayectos_por_pnf(self, *args):
        nombre_pnf = self.pnf_var.get()
        if nombre_pnf not in self.pnf_id_por_nombre:
            self.option_menu_trayecto.configure(values=["No seleccionado"])
            self.trayecto_var.set("No seleccionado")
            self.option_menu_tramo.configure(values=["No seleccionado"])
            self.tramo_var.set("No seleccionado")
            self.trayecto_id_por_nombre = {}
            self.tramo_id_por_nombre = {}
            return

        pnf_id = self.pnf_id_por_nombre[nombre_pnf]
        self.lista_trayectos = self.controlador.obtener_trayectos_por_pnf(pnf_id)
        self.trayecto_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.lista_trayectos}
        
        self.nombre_trayecto = [tupla[1] for tupla in self.lista_trayectos] or ["Sin opciones disponibles"]
        self.nombre_trayecto.insert(0,"No seleccionado")

        self.option_menu_trayecto.configure(values=self.nombre_trayecto)
        # self.trayecto_var.set(self.nombre_trayecto[0])
        # Reset tramos
        self.option_menu_tramo.configure(values=["No seleccionado"])
        self.tramo_var.set("No seleccionado")
        self.tramo_id_por_nombre = {}

    def actualizar_tramos_por_trayecto(self, *args):
        nombre_trayecto = self.trayecto_var.get()
        if not hasattr(self, 'trayecto_id_por_nombre') or nombre_trayecto not in self.trayecto_id_por_nombre:
            self.option_menu_tramo.configure(values=["No seleccionado"])
            # self.tramo_var.set("Seleccionar")
            self.tramo_id_por_nombre = {}
            return

        trayecto_id = self.trayecto_id_por_nombre[nombre_trayecto]
        self.lista_tramos = self.controlador.obtener_tramos_por_trayecto(trayecto_id)
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.lista_tramos}
        
        self.nombre_tramo = [tupla[1] for tupla in self.lista_tramos] or ["Sin opciones disponibles"]
        self.nombre_tramo.insert(0,"No seleccionado")

        self.option_menu_tramo.configure(values=self.nombre_tramo)
        # self.tramo_var.set(self.nombre_tramo[0])

    def ejecutar_busqueda(self):
        nombre_pnf = self.pnf_var.get()
        nombre_trayecto = self.trayecto_var.get()
        nombre_tramo = self.tramo_var.get()

        if nombre_pnf not in self.pnf_id_por_nombre:
            messagebox.showerror("Error", "Por favor, seleccione un PNF válido.")
            return

        id_pnf = self.pnf_id_por_nombre.get(nombre_pnf)
        id_trayecto = self.trayecto_id_por_nombre.get(nombre_trayecto) if hasattr(self, 'trayecto_id_por_nombre') else None
        id_tramo = self.tramo_id_por_nombre.get(nombre_tramo) if hasattr(self, 'tramo_id_por_nombre') else None
        
        # Lógica de búsqueda según los filtros seleccionados
        if not id_trayecto and not id_tramo:
            lista_uc = self.controlador.buscar_uc_por_pnf_trayecto_tramo(id_pnf)
        elif id_trayecto and not id_tramo:
            lista_uc = self.controlador.buscar_uc_por_pnf_trayecto_tramo(id_pnf, id_trayecto)
        elif id_trayecto and id_tramo:
            lista_uc = self.controlador.buscar_uc_por_pnf_trayecto_tramo(id_pnf, id_trayecto, id_tramo)
        else:
            lista_uc = []

        self.master.calcular_pagina(lista_uc)
        self.master.actualizar_pagina()

    def obtener_nombre_pnf(self):
            """Obtiene los nombres completos de los PNFs"""
            return [tupla[2] for tupla in self.lista_pnf] if self.lista_pnf else []