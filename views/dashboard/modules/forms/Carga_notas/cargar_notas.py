import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class CargaNotasFrame(SectionFrameBase):
    def __init__(self, master, controller_periodos_academicos, controller_pnf, controller_secciones):
        super().__init__(master, "Gestion De Carga de Notas")
        
        self.controller_pnf = controller_pnf
        self.controller_periodos_academicos = controller_periodos_academicos
        self.controller_secciones = controller_secciones
        
        self.nombres_periodos = self.controller_periodos_academicos.obtener_nombres_periodos()
        self.var_periodo = ctk.StringVar(value=self.nombres_periodos[0])
        
        
        self.tuple_pnf = self.controller_pnf.listado_pnf
        self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
        self.var_pnf = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "")
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}  # nombre: id
        
        pnf_id_inicial = self.pnf_id_por_nombre[self.var_pnf.get()]
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(pnf_id_inicial)
        self.var_seccion = ctk.StringVar(value=self.secciones_disponibles[0] if self.secciones_disponibles else "Sin secciones")
        
        
        self.pnf_menu = create_option_menu_row(self, "Seleccione un P.N.F:", self.nombres_pnf, self.var_pnf, funcion=self.actualizar_secciones)
        self.periodo_menu = create_option_menu_row(self, "Seleccionar Periodo Académico:", self.nombres_periodos, self.var_periodo)
        self.seccion_menu = create_option_menu_row(self, "Seleccione una Sección:", self.secciones_disponibles, self.var_seccion)
        
           

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def actualizar_secciones(self, nombre_pnf):

        pnf_id = self.pnf_id_por_nombre[nombre_pnf]
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(pnf_id)
        self.var_seccion.set(self.secciones_disponibles[0] if self.secciones_disponibles else "Sin secciones")
        self.seccion_menu.configure(values=self.secciones_disponibles)

    def obtener_filtros_seleccionados(self):

        periodo_id = self.controller_periodos_academicos.obtener_id_por_nombre(self.var_periodo.get())
        pnf_id = self.pnf_id_por_nombre[self.var_pnf.get()]
        seccion_id = self.controller_secciones.obtener_id_por_nombre(self.var_seccion.get())
        return (periodo_id, pnf_id, seccion_id)
    