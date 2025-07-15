import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from controllers.dashboard.PNF.controller_pnf import ControllerPNF

from ..DatosPersonales import DatosPersonalesFrame

class FremeSecciones(SectionFrameBase):
    def __init__(self, master, controlador_docentes, controlador_pnf, titulo="Datos de Secciones"):
        super().__init__(master, titulo)
        self.controlador_Doc = controlador_docentes
        self.nombres_docentes = self.controlador_Doc.obtener_nombres_docentes()
        
        self.controller_pnf = controlador_pnf
        self.nombres_pnf = self.controlador_pnf.obtener_nombres_pnf()

        #variables de control
        self.var_docente = ctk.StringVar(value=self.nombres_docentes[0])
        self.var_turno = ctk.StringVar(value="Diurno")
        self.var_modalidad = ctk.StringVar(value="Presencial")
        self.var_estado = ctk.StringVar(value="Planificación")

        #Obterner datos pnf, trayecto y tramo
        self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
        self.var1 = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "") # Valor por defecto para el PNF
        
        self.tuple_pnf = self.controller_pnf.listado_pnf
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}  # nombre: id

        self.trayecto_id_por_nombre = {trayecto[1]: trayecto[0] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])}  # nombre: id
        self.valores_trayecto = [trayecto[1] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])]  # Obtener los trayectos para el PNF seleccionado

        self.tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[self.var_trayecto.get()])  # Obtener los tramos para el trayecto seleccionado
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.tupla_tramos}  # nombre: id
        self.valores_tramos = [tramo[1] for tramo in self.tupla_tramos]
    
        self.var_tramo = ctk.StringVar(value=self.valores_tramos[0] if self.valores_tramos else "No seleccionado")  # Valor por defecto para el tramo

        self._crear_fila_widgets([
            ("Seleccione un P.N.F:", crear_option_menu, {"values":self.nombres_pnf, "variable":self.var1, "command": self.set_trayecto  }, 1, self, 'pnf_menu'),
            ("Trayecto Actual:", crear_option_menu, {"values": self.valores_trayecto, "variable": self.var_trayecto,"command": self.set_tramo}, 1, self, 'trayecto_menu'),
            ("Tramo Actual:", crear_option_menu, {"values": self.valores_tramos, "variable": self.var_tramo}, 1, self, 'tramo_menu'),
        ])

        self._crear_fila_widgets([
            ("Codigo", crear_entry, {"width": 300, "placeholder_text": "Ingrese el codigo"}, 1, self, "codigo_entry"),
            ("Docente", crear_option_menu,{"values": self.nombres_docentes,"variable": self.var_docente,"width": 300}, 1, self, "docente_menu"),
            ("Cupo Máximo", crear_entry, {"width": 300, "placeholder_text":"Cupo Máximo"},1, self, "cupo_maximo_entry"),
            ("Turno", crear_option_menu, {"values": ["Diurno", "Nocturno", "Fin de Semana"], "variable": self.var_turno, "width": 300}, 1, self, "turno_menu"),
            ("Modalidad", crear_option_menu, {"values": ["Presencial","Semipresencial","Virtual"],"variable": self.var_modalidad,"width": 300}, 1, self, "modalidad_menu"),
            ("Aula", crear_entry, {"width": 300, "placeholder_text": "Ingrese el aula"}, 1, self, "aula_entry"),
            ("Estado", crear_option_menu, {"values": ["Planificación","Abierta","En Curso","Finalizado","Cancelada","Suspendida"],"variable": self.var_estado, "width": 200},1,self,"estado_menu")
        ])
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def set_trayecto(self, value):
        tupla_trayectos = self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[value])
        self.trayecto_id_por_nombre = {trayecto[1]: trayecto[0] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])}  # nombre: id
        self.valores_trayecto = [trayecto[1] for trayecto in tupla_trayectos]  # Obtener solo los nombres de los trayectos
        self.var_trayecto.set(self.valores_trayecto[0] if self.valores_trayecto else "Trayecto")  # Valor por defecto para el trayecto

        self.trayecto_menu.configure(values=self.valores_trayecto)
        print("Trayectos disponibles:", self.valores_trayecto)

    def set_tramo(self, value):
        tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[value])
        self.valores_tramos = [tramo[1] for tramo in tupla_tramos]
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.tupla_tramos}  # nombre: id
        self.var_tramo.set(self.valores_tramos[0] if self.valores_tramos else "Tramo")
        self.tramo_menu.configure(values=self.valores_tramos)

    def obtener_tupla_pnf(self):
        self.trayecto_id_por_nombre = {trayecto[1]: trayecto[0] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])}  # nombre: id
        self.tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[self.var_trayecto.get()])
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.tupla_tramos}  # nombre: id
        return (self.pnf_id_por_nombre[self.pnf_menu.get()],self.trayecto_id_por_nombre[self.trayecto_menu.get()],self.tramo_id_por_nombre[self.tramo_menu.get()],self.trayecto_menu.get(),self.tramo_menu.get())