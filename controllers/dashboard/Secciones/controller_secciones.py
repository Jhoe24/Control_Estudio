import tkinter.messagebox as messagebox
from models.Secciones.models_secciones import ModeloSecciones
from datetime import datetime

import os
import sqlite3

class ControllerSecciones:

    def __init__(self):
        self.modelo = ModeloSecciones()
        self._seccion_id_por_nombre = {}
    
    def obtener_datos_vista(self, vista):
        
        sede_id = vista.controller_sede.obtener_id_por_codigo(vista.var_sede.get())
        periodo_academico_id = vista.controller_PA.obtener_id_por_codigo(vista.var_periodo.get())

        for id_nombre in vista.id_nombres_docentes:
            if id_nombre[1] == vista.var_docente.get():
                docente_titular_id = id_nombre[0]
                break

        datos = {
            "sede_id": sede_id,
            "periodo_academico_id": periodo_academico_id,
            "codigo_seccion": vista.codigo_entry.get(),
            "docente_titular_id": docente_titular_id,
            "cupo_maximo": vista.cupo_maximo_entry.get(),
            "turno": vista.var_turno.get(),
            "modalidad": vista.var_modalidad.get(),
            "aula": vista.aula_entry.get(),
            "estado": vista.var_estado.get(),
            "pnf_id": vista.pnf_id_por_nombre[vista.var1.get()],
            "trayecto_id": vista.trayecto_id_por_nombre[vista.var_trayecto.get()],
            "tramo_id": vista.tramo_id_por_nombre[vista.var_tramo.get()]
        }
        return datos
    
    def campos_obligatorios(self, vista, datos):
       
        alias=[
            ("codigo_seccion", "Codigo"),
            ("cupo_maximo", "Cupo Máximo"),
            ("aula", "Aula")
        ]

        for campo,nombre_mostrar in alias:
            if datos[campo] == "" or datos[campo] == None:
                messagebox.showwarning("Campo Vacío", f"El campo '{nombre_mostrar}' es obligatorio.", parent=vista)
                return False
        return True
        
    def registrar_seccion(self,datos, vista):
        exito = self.modelo.registrar_sede(datos)

        if exito:
            messagebox.showinfo(title="Exito",message="Se registro la seccion correctamente", parent=vista)
            return True
        else:
            messagebox.showerror(title="Error",message="No se pudo registrar la seccion", parent=vista)
            return False
        
    def listar_secciones(self, id_pnf):
        return self.modelo.listar_secciones(id_pnf)
    
    def limpiar_formulario_completo(self, vista):
        pass

    def obtener_nombres_secciones_por_pnf(self, pnf_id, trayecto_id = None, tramo_id = None):
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'db', 'Sistema_academico.db')
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        
        if trayecto_id and tramo_id:
            sql = """
                SELECT s.id, s.codigo_seccion || ' - ' || s.turno AS nombre
                FROM secciones s
                WHERE s.pnf_id = ? AND s.trayecto_id = ? AND tramo_id = ?
                ORDER BY s.codigo_seccion 
            """
            tupla_datos = (pnf_id,trayecto_id,tramo_id)     
        else:
            sql = """
                SELECT s.id, s.codigo_seccion || ' - ' || s.turno AS nombre
                FROM secciones s
                WHERE s.pnf_id = ?
                ORDER BY s.codigo_seccion
            """
            tupla_datos = (pnf_id,)

        cursor.execute(sql,tupla_datos)

        resultados = cursor.fetchall()

        conn.close()

        self._seccion_id_por_nombre = {nombre: id for id, nombre in resultados}
        return list(self._seccion_id_por_nombre.keys())
    
    def obtener_fecha_actual(self):
        return datetime.now().strftime("%Y-%m-%d")

    def obtener_id_por_nombre(self, nombre_seccion):
        return self._seccion_id_por_nombre.get(nombre_seccion)

    def actualizar_seccion(self, seccion_id, datos_actualizados, ventana):
        exito = self.modelo.actualizar_seccion(seccion_id, datos_actualizados,self.obtener_fecha_actual())
        if exito:
            messagebox.showinfo("Éxito", "Datos de la sección actualizados correctamente.", parent=ventana)
            return True
        else:
            messagebox.showerror("Error", "No se pudo actualizar los datos de la sección.", parent=ventana)
            return False
        
    def obtener_nombre_docente_por_id(self, docente_id, pnf_id):
        listado = self.controlador_docentes.obtener_solo_nombres_docentes_por_pnf(pnf_id)
        for id, nombre in listado:
            if id == docente_id:
                return nombre
        return ""
    
    def obtener_datos_vista_seccionAsignada(self, vista):
        name_seccion = vista.var_seccion.get()
        seccion_id = self.obtener_id_por_nombre(name_seccion)
        return {
            "seccion_id":seccion_id,
            "condicion":vista.var_condicion.get(),
            "estado":vista.var_estado.get()
        }
    
    def registrar_estudiante_seccion(self,datos):
        """Verificar si ya existe dicha asignacion para armar la consulta"""
        sql = """SELECT * FROM inscripciones WHERE estudiante_id = ?"""

        resultado = self.modelo.ejecutar_consulta_armada(sql,(datos["estudiante_id"],),True)
        """Si la asignacion ya existe actualizarla y si no insertar una nueva"""
        if resultado:
            sql="""UPDATE inscripciones SET condicion = ?, estado = ?, seccion_id = ? WHERE estudiante_id = ?"""
            return self.modelo.ejecutar_consulta_armada(sql,(datos["condicion"],
                                                             datos["estado"],
                                                             datos["seccion_id"],
                                                             datos["estudiante_id"]))
        else:
            sql = """INSERT INTO inscripciones (estudiante_id, seccion_id, condicion, estado) VALUES (?,?,?,?)"""
            return self.modelo.ejecutar_consulta_armada(sql,(datos["estudiante_id"],
                                                             datos["seccion_id"],
                                                             datos["condicion"],
                                                             datos["estado"]))
    
    def obtener_nombre_por_id(self, id_seccion):
        sql = """SELECT codigo_seccion FROM secciones WHERE id = ?"""
        resultado = self.modelo.ejecutar_consulta_armada(sql,(id_seccion,),True)
        if resultado:
            return resultado
        else:
            return None
        
    def obtener_seccion_estudiante(self, estudiante_id):
        sql = """SELECT * FROM inscripciones WHERE estudiante_id = ?"""
        resultado = self.modelo.ejecutar_consulta_armada(sql,(estudiante_id,),True)
        if resultado:
            return resultado
        else:
            return None
        
