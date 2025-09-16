import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
#from controllers.dashboard.PNF.controller_pnf import ControllerPNF

from ..DatosPersonales import DatosPersonalesFrame

class FremeSecciones(SectionFrameBase):
    def __init__(self, master, controlador_docentes, controlador_pnf, controller_seccion, controller_sede, controller_PA, titulo="Datos de Secciones", fgcolor=COLOR_HEADER_SECCION_BG):
        super().__init__(master, titulo,fgcolor)
        self.controlador_Doc = controlador_docentes
        self.controller_pnf = controlador_pnf   
        self.controller_secciones = controller_seccion
        self.controller_PA = controller_PA
        self.controller_sede = controller_sede

        self.nombres_docentes = []
        #variables de control
        self.var_turno = ctk.StringVar(value="Diurno")
        self.var_modalidad = ctk.StringVar(value="Presencial")
        self.var_estado = ctk.StringVar(value="Planificada")
        
        # Obtener lista completa de sedes 
        self.listado_sedes_completo = self.controller_sede.listar_sedes()

        self.sedes = self.controller_sede.obtener_codigos()
        if self.sedes:
            self.var_sede = ctk.StringVar(value=self.sedes[0])
        else:
            self.var_sede = ctk.StringVar(value="No hay sedes")

        self.periodos_academicos = self.controller_PA.obtener_codigos()
        if self.periodos_academicos:
            self.var_periodo = ctk.StringVar(value=self.periodos_academicos[0])
        else:
            self.var_periodo = ctk.StringVar(value="No hay Periodos Academicos")
        
        #Obterner datos pnf, trayecto y tramo
        self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
        self.var1 = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "") # Valor por defecto para el PNF
        
        self.tuple_pnf = self.controller_pnf.listado_pnf
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}  # nombre: id

        self.id_nombres_docentes = self.controlador_Doc.obtener_solo_nombres_docentes_por_pnf(self.pnf_id_por_nombre[self.var1.get()])

        if self.id_nombres_docentes:
            for id_nombre in self.id_nombres_docentes:
                self.nombres_docentes.append(id_nombre[1])

        if self.nombres_docentes:
            self.var_docente = ctk.StringVar(value=self.nombres_docentes[0])
        else:
            self.var_docente = ctk.StringVar(value="No hay Docentes Asignado")

        self.trayecto_id_por_nombre = {trayecto[1]: trayecto[0] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])}  # nombre: id
        self.valores_trayecto = [trayecto[1] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])]  # Obtener los trayectos para el PNF 
        
        self.var_trayecto = ctk.StringVar(value=self.valores_trayecto[0] if self.valores_trayecto else "Trayecto")  # Valor por defecto para el trayecto
        self.tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[self.var_trayecto.get()])  # Obtener los tramos para el trayecto 
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.tupla_tramos}  # nombre: id
        self.valores_tramos = [tramo[1] for tramo in self.tupla_tramos]
    
        self.var_tramo = ctk.StringVar(value=self.valores_tramos[0] if self.valores_tramos else "No seleccionado")  # Valor por defecto para el tramo

        self._crear_fila_widgets([
            ("Sede:", crear_option_menu, {"values":self.sedes, "variable":self.var_sede }, 1, self, 'sede_menu'),
            ("Seleccione un Periodo Académico:", crear_option_menu, {"values":self.periodos_academicos, "variable":self.var_periodo }, 1, self, 'periodo_menu'),
        ])

        self._crear_fila_widgets([
            ("Seleccione un P.N.F:", crear_option_menu, {"values":self.nombres_pnf, "variable":self.var1, "command": self.set_trayecto  }, 1, self, 'pnf_menu'),
            ("Trayecto Actual:", crear_option_menu, {"values": self.valores_trayecto, "variable": self.var_trayecto,"command": self.set_tramo}, 1, self, 'trayecto_menu'),
            ("Tramo Actual:", crear_option_menu, {"values": self.valores_tramos, "variable": self.var_tramo}, 1, self, 'tramo_menu'),
        ])

        self._crear_fila_widgets([
            ("Codigo", crear_entry, {"width": 300, "placeholder_text": "Ingrese el codigo"}, 1, self, "codigo_entry"),
            ("Docente", crear_option_menu,{"values": self.nombres_docentes,"variable": self.var_docente,"width": 300}, 1, self, "docente_menu"),
            ("Cupo Máximo", crear_entry, {"width": 300, "placeholder_text":"Cupo Máximo"},1, self, "cupo_maximo_entry"),
            ("Turno", crear_option_menu, {"values": ["Diurno", "Nocturno", "Fin de semana"], "variable": self.var_turno, "width": 300}, 1, self, "turno_menu"),
            ("Modalidad", crear_option_menu, {"values": ["Presencial","Semipresencial","Virtual"],"variable": self.var_modalidad,"width": 300}, 1, self, "modalidad_menu"),
            ("Aula", crear_entry, {"width": 300, "placeholder_text": "Ingrese el aula"}, 1, self, "aula_entry"),
            ("Estado", crear_option_menu, {"values": ["Planificada","Abierta","En curso","Finalizada","Cancelada","Suspendida"],"variable": self.var_estado, "width": 200},1,self,"estado_menu")
        ])
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def set_trayecto(self, value):
        tupla_trayectos = self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[value])
        self.trayecto_id_por_nombre = {trayecto[1]: trayecto[0] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])}  # nombre: id
        self.valores_trayecto = [trayecto[1] for trayecto in tupla_trayectos]  # Obtener solo los nombres de los trayectos
        self.var_trayecto.set(self.valores_trayecto[0] if self.valores_trayecto else "Trayecto")  # Valor por defecto para el trayecto

        self.id_nombres_docentes = self.controlador_Doc.obtener_solo_nombres_docentes_por_pnf(self.pnf_id_por_nombre[value])

        self.nombres_docentes = []
        for id_nombre in self.id_nombres_docentes:
            self.nombres_docentes.append(id_nombre[1])

        self.var_docente.set(self.nombres_docentes[0] if self.nombres_docentes else "No hay Docentes Asignado")
        self.trayecto_menu.configure(values=self.valores_trayecto)
        print("Trayectos disponibles:", self.valores_trayecto)

    def set_tramo(self, value):
        self.tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[value])
        self.valores_tramos = [tramo[1] for tramo in self.tupla_tramos]
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.tupla_tramos}  # nombre: id
        self.var_tramo.set(self.valores_tramos[0] if self.valores_tramos else "Tramo")
        self.tramo_menu.configure(values=self.valores_tramos)

    def obtener_tupla_pnf(self):
        self.trayecto_id_por_nombre = {trayecto[1]: trayecto[0] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])}  # nombre: id
        self.tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[self.var_trayecto.get()])
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.tupla_tramos}  # nombre: id
        return (self.pnf_id_por_nombre[self.pnf_menu.get()],self.trayecto_id_por_nombre[self.trayecto_menu.get()],self.tramo_id_por_nombre[self.tramo_menu.get()])
    
    def obtener_datos_vista(self):
        return self.controller_secciones.obtener_datos_vista(self)

    def habilitar_campos(self):
        self.codigo_entry.configure(state="normal")
        self.docente_menu.configure(state="normal")
        self.cupo_maximo_entry.configure(state="normal")
        self.turno_menu.configure(state="normal")
        self.modalidad_menu.configure(state="normal")
        self.aula_entry.configure(state="normal")
        self.estado_menu.configure(state="normal")
        self.sede_menu.configure(state="normal")
        self.periodo_menu.configure(state="normal")
        self.pnf_menu.configure(state="normal")
        self.trayecto_menu.configure(state="normal")
        self.tramo_menu.configure(state="normal")
        
    def deshabilitar_campos(self):
        self.codigo_entry.configure(state="disabled")
        self.docente_menu.configure(state="disabled")
        self.cupo_maximo_entry.configure(state="disabled")
        self.turno_menu.configure(state="disabled")
        self.modalidad_menu.configure(state="disabled")
        self.aula_entry.configure(state="disabled")
        self.estado_menu.configure(state="disabled")
        self.sede_menu.configure(state="disabled")
        self.periodo_menu.configure(state="disabled")
        self.pnf_menu.configure(state="disabled")
        self.trayecto_menu.configure(state="disabled")
        self.tramo_menu.configure(state="disabled")

    def cargar_datos(self, datos):
        try:
            # Recargar Mapeos
            self.listado_sedes_completo = self.controller_sede.listar_sedes()
            self.sedes_nombres = [s['nombre'] for s in self.listado_sedes_completo]
            self.sede_id_to_nombre = {s['id']: s['nombre'] for s in self.listado_sedes_completo}
            self.sede_codigo_to_nombre = {s['codigo']: s['nombre'] for s in self.listado_sedes_completo}

            self.listado_pa_completo = self.controller_PA.obtener_periodos_academicos()
            self.periodos_academicos_nombres = self.controller_PA.obtener_nombres_periodos()
            self.pa_id_to_nombre = {pa['id']: pa['nombre'] for pa in self.listado_pa_completo}
            
            # Código
            self.codigo_entry.delete(0, "end")
            codigo_val = datos.get("codigo_seccion", "")
            if codigo_val:
                self.codigo_entry.insert(0, codigo_val)
            self.codigo_entry.configure(state="disabled")

            # Docente
            docente_nombre = datos.get("docente_titular_id", "")
            pnf_nombre = datos.get("pnf_id", "")
            if pnf_nombre:
                pnf_id = self.pnf_id_por_nombre.get(pnf_nombre)
                if pnf_id:
                    self.id_nombres_docentes = self.controlador_Doc.obtener_solo_nombres_docentes_por_pnf(pnf_id)
                    self.nombres_docentes = [doc[1] for doc in self.id_nombres_docentes]
                    self.docente_menu.configure(values=self.nombres_docentes)

                    if docente_nombre and docente_nombre in self.nombres_docentes:
                        self.var_docente.set(docente_nombre)
                    else:
                        self.var_docente.set("No hay Docentes Asignado")

            self.docente_menu.configure(state="disabled")

            # Cupo Máximo
            self.cupo_maximo_entry.delete(0, "end")
            cupo_val = datos.get("cupo_maximo", "")
            if cupo_val:
                self.cupo_maximo_entry.insert(0, str(cupo_val))
            self.cupo_maximo_entry.configure(state="disabled")

            # Turno
            turno_val = datos.get("turno", "Diurno")
            if turno_val in ["Diurno", "Nocturno", "Fin de semana"]:
                self.var_turno.set(turno_val)
            else:
                self.var_turno.set("Diurno")
            self.turno_menu.configure(state="disabled")

            # Modalidad
            modalidad_val = datos.get("modalidad", "Presencial")
            if modalidad_val in ["Presencial", "Semipresencial", "Virtual"]:
                self.var_modalidad.set(modalidad_val)
            else:
                self.var_modalidad.set("Presencial")
            self.modalidad_menu.configure(state="disabled")

            # Aula
            self.aula_entry.delete(0, "end")
            aula_val = datos.get("aula", "")
            if aula_val:
                self.aula_entry.insert(0, aula_val)
            self.aula_entry.configure(state="disabled")

            # Estado
            estado_val = datos.get("estado", "Planificada")
            if estado_val in ["Planificada", "Abierta", "En curso", "Finalizada", "Cancelada", "Suspendida"]:
                self.var_estado.set(estado_val)
            else:
                self.var_estado.set("Planificación")
            self.estado_menu.configure(state="disabled")

            # Sede
            sede_val = datos.get("sede_id", "")
            resultado = self.controller_sede.obtener_codigo_por_id(sede_val)
            if resultado:
                sede_val = resultado
            if sede_val in self.sedes:
                self.var_sede.set(sede_val)
            else:
                self.var_sede.set("Sede no seleccionada")
            self.sede_menu.configure(state="disabled")

            # Periodo Académico
            periodo_val = datos.get("periodo_academico_id", "")
            resultado = self.controller_PA.obtener_codigo_por_id(periodo_val)
            if resultado:
                periodo_val = resultado
            if periodo_val in self.periodos_academicos:
                self.var_periodo.set(periodo_val)
            else:
                self.var_periodo.set("Periodo académico no seleccionado")
            self.periodo_menu.configure(state="disabled")

            # PNF
            pnf_val = datos.get("pnf_id", "")
            if pnf_val in self.nombres_pnf:
                self.var1.set(pnf_val)
                # Actualizar trayectos y tramos 
                self.set_trayecto(pnf_val)
                
                # Actualizar docentes
                pnf_id = self.pnf_id_por_nombre.get(pnf_val)
                if pnf_id:
                    self.id_nombres_docentes = self.controlador_Doc.obtener_solo_nombres_docentes_por_pnf(pnf_id)
                    self.nombres_docentes = [doc[1] for doc in self.id_nombres_docentes]
                    self.docente_menu.configure(values=self.nombres_docentes)
                    
                    docente_nombre = datos.get("docente_titular_id", "")
                    if docente_nombre in self.nombres_docentes:
                        self.var_docente.set(docente_nombre)
            else:
                self.var1.set(self.nombres_pnf[0] if self.nombres_pnf else "")
                self.set_trayecto(self.var1.get())
            self.pnf_menu.configure(state="disabled")

            # Trayecto
            trayecto_val = datos.get("trayecto_id", "")
            if trayecto_val in self.valores_trayecto:
                self.var_trayecto.set(trayecto_val)
                # Actualizar tramos 
                self.set_tramo(trayecto_val)
            else:
                self.var_trayecto.set(self.valores_trayecto[0] if self.valores_trayecto else "Trayecto")
                self.set_tramo(self.var_trayecto.get())
            self.trayecto_menu.configure(state="disabled")
            
            # Tramo
            tramo_val = datos.get("tramo_id", "")
            if tramo_val in self.valores_tramos:
                self.var_tramo.set(tramo_val)
            else:
                self.var_tramo.set(self.valores_tramos[0] if self.valores_tramos else "No seleccionado")
            self.tramo_menu.configure(state="disabled")

        except Exception as e:
            print(f"Error al cargar datos en el formulario de secciones: {e}")
