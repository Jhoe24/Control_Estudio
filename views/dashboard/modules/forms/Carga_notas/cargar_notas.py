import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class CargaNotasFrame(SectionFrameBase):
    def __init__(self, master, controller_periodos_academicos, controller_pnf, controller_secciones, docente_id = None, rol = None):
        super().__init__(master, "Gestion De Carga de Notas")
        
        self.controller_pnf = controller_pnf
        self.controller_periodos_academicos = controller_periodos_academicos
        self.controller_secciones = controller_secciones
        self.docente_id = docente_id
        self.rol = rol

        self.nombres_periodos = self.controller_periodos_academicos.obtener_nombres_periodos()
        if not self.nombres_periodos:
            self.nombres_periodos = ["No hay periodos"]
        self.var_periodo = ctk.StringVar(value=self.nombres_periodos[0])
        
        if docente_id:
            self.tuple_pnf = self.controller_pnf.obtener_pnf_asignado_docente(docente_id)
        else:
            self.tuple_pnf = self.controller_pnf.listado_pnf
        
        self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
        self.var_pnf = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "")
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}  # nombre: id
        
        pnf_id_inicial = self.pnf_id_por_nombre[self.var_pnf.get()]
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(pnf_id_inicial)
        self.var_seccion = ctk.StringVar(value=self.secciones_disponibles[0] if self.secciones_disponibles else "Sin secciones")
        
        
        self.pnf_menu = create_option_menu_row(self, "Seleccione un P.N.F:", self.nombres_pnf, self.var_pnf, funcion=self.actualizar_secciones)
        self.periodo_menu = create_option_menu_row(self, "Seleccionar Periodo Académico:", self.nombres_periodos, self.var_periodo)
        if not self.docente_id:
            self.seccion_menu = create_option_menu_row(self, "Seleccione una Sección:", self.secciones_disponibles, self.var_seccion)
        
           

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def actualizar_secciones(self, nombre_pnf):
        if self.docente_id:
            return
        pnf_id = self.pnf_id_por_nombre[nombre_pnf]
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(pnf_id)
        self.var_seccion.set(self.secciones_disponibles[0] if self.secciones_disponibles else "Sin secciones")
        self.seccion_menu.configure(values=self.secciones_disponibles)

    def obtener_filtros_seleccionados(self):
    
        periodo_id = self.controller_periodos_academicos.obtener_id_por_nombre(self.var_periodo.get())
        pnf_id = self.pnf_id_por_nombre[self.var_pnf.get()]
        if self.docente_id:
           """En caso tal de que docente_id sea diferente de None necesito 
           obtener todas el id pnf y el id del periodo academico"""
           sql = """
                SELECT id FROM docente_sede_pnf WHERE docente_id = ? AND pnf_id = ?
            """
           datos = self.controller_secciones.modelo.ejecutar_consulta_armada(sql, (self.docente_id, pnf_id,), True)
         
           return (pnf_id, periodo_id, datos.get('id'))#retorna pnf_id, periodo_id, docente_pnf_id
        else: 
            seccion_id = self.controller_secciones.obtener_id_por_nombre(self.var_seccion.get())
            sql = """
                SELECT trayecto_id, tramo_id FROM secciones WHERE id = ?
            """
            datos = self.controller_secciones.modelo.ejecutar_consulta_armada(sql, (seccion_id,), True)
            if datos:
                trayecto_id = datos.get('trayecto_id')
                tramo_id = datos.get('tramo_id')
            else:
                trayecto_id = None
                tramo_id = None

            # Obtener los nombres seleccionados
            trayecto_nombre = None
            tramo_nombre = None
            if trayecto_id:
                # Buscar nombre trayecto
                trayectos = self.controller_pnf.obtener_trayectos_por_pnf(pnf_id)
                trayecto_id_por_nombre = {t[1]: t[0] for t in trayectos}
                trayecto_nombre = next((nombre for nombre, tid in trayecto_id_por_nombre.items() if tid == trayecto_id), None)
            if tramo_id:
                # Buscar nombre tramo
                tramos = self.controller_pnf.obtener_tramos_por_trayecto(trayecto_id)
                tramo_id_por_nombre = {t[1]: t[0] for t in tramos}
                tramo_nombre = next((nombre for nombre, tid in tramo_id_por_nombre.items() if tid == tramo_id), None)

            return (pnf_id, trayecto_id, tramo_id, trayecto_nombre, tramo_nombre, seccion_id)
        
    
   
