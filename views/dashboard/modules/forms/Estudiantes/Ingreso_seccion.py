import tkinter.messagebox as messagebox
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class AsignarSeccionFrame(SectionFrameBase):
    def __init__(self, master, controller_secciones,pnf_id, trayecto_id, tramo_id):
        super().__init__(master,"Asignar Secciones a Estudiante",COLOR_HEADER_SECCION_BG_2)
        self.controller_secciones = controller_secciones
        self.pnf_id = pnf_id
        self.trayecto_id = trayecto_id
        self.tramo_id = tramo_id
        self.var_seccion = None
        #Secciones_disponibles es donde se extraen los datos de las secciones asignadas a ese pnf
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(self.pnf_id,trayecto_id,tramo_id)
        if self.secciones_disponibles:
            
            self.var_seccion = ctk.StringVar(value=self.secciones_disponibles[0] if self.secciones_disponibles else "Sin secciones")
            self.var_condicion = ctk.StringVar(value="Regular")
            self.var_estado = ctk.StringVar(value="Inscrito")


            self._crear_fila_widgets([
                ("Secciones Disponibles:",crear_option_menu,{"values":self.secciones_disponibles,"variable":self.var_seccion},1,self,"secciones_menu"),
                ("Condición:",crear_option_menu,{"values":["Regular","Equivalencia","Repitente","Especial","Oyente"],"variable":self.var_condicion},1,self,"condicion_menu"),
                ("Estado:",crear_option_menu,{"values":["Inscrito","Retirado","Aprobado","Reprobado","Sin Calificar"],"variable":self.var_estado},1,self,"estado_menu")         

            ])

            
        else:   
            master.no_secciones_disponibles()


    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def actualizar_datos_secciones(self,pnf_id,trayecto_id,tramo_id):
        self.pnf_id = pnf_id
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(self.pnf_id,trayecto_id,tramo_id)
        if not self.secciones_disponibles:
            self.var_seccion.set("Sin secciones")
            self.secciones_menu.configure(values=["Sin secciones"],state = "disabled")
        else:
            self.secciones_menu.configure(state = "normal")
            self.var_seccion.set(self.secciones_disponibles[0])
            self.secciones_menu.configure(values=self.secciones_disponibles)

        # if not self.secciones_disponibles:
        #     # Si no hay secciones disponibles, hacemos como en el master.no_secciones_disponibles()
        #     self.master.no_secciones_disponibles()


    def cargar_datos_secciones(self, datos):
        if datos["seccion_id"]:
            nombre = self.controller_secciones.obtener_nombre_por_id(datos["seccion_id"])
            if self.var_seccion:
                self.var_seccion.set(nombre["codigo_seccion"])
        self.secciones_menu.configure(state="disabled")

        self.var_condicion.set(datos["condicion"])
        self.condicion_menu.configure(state="disabled")

        self.var_estado.set(datos["estado"])
        self.estado_menu.configure(state="disabled")
    
    def habilitar_campos(self):
        self.secciones_menu.configure(state="normal")
        self.condicion_menu.configure(state="normal")
        self.estado_menu.configure(state="normal")

        
