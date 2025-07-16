import tkinter.messagebox as messagebox
from models.Periodo_Academico.modeloProAcd import ModeloProAcademico

class PeriodoAcademicoController:
    def __init__(self):
        self.modelo_pa= ModeloProAcademico()

    def registrar_periodo_academico(self, datos_periodo, vista_formulario):
        """Registrar Periodos Academicos"""       
        resultado = self.modelo_pa.registrar_periodo_academico(datos_periodo)
        if resultado:
            messagebox.showinfo("Registro Exitoso", "El periodo académico ha sido registrado exitosamente.", parent=vista_formulario)
            return True
        else:
            messagebox.showerror("Error", "No se pudo registrar el periodo académico.", parent=vista_formulario)
            return False

    def obtener_datos_vista(self, vista_formulario):
        """Obtener datos de la vista"""
        dic_estado = {
            "Planificación": "planificacion",
            "Inscripción": "inscripcion",
            "En Curso": "en_curso",
            "Evaluaciones": "evaluaciones",
            "Finalizado": "finalizado",
            "Cerrado": "cerrado"
        }
        print("Estado seleccionado:", vista_formulario.var_estado.get())
        datos_periodo = {
            "codigo": vista_formulario.codigo_entry.get(),
            "nombre": vista_formulario.nombre_entry.get(),
            "tipo": vista_formulario.var_tipo.get(),
            "fecha_inicio": vista_formulario.fecha_inicio,
            "fecha_fin": vista_formulario.fecha_fin,
            "fecha_inicio_inscripcion": vista_formulario.fecha_inicio_inscripcion,   
            "fecha_fin_inscripcion": vista_formulario.fecha_fin_inscripcion,
            "fecha_inicio_clases": vista_formulario.fecha_inicio_clases,
            "fecha_fin_clases": vista_formulario.fecha_fin_clases,
            "fecha_inicio_evaluaciones": vista_formulario.fecha_inicio_evaluaciones,
            "fecha_fin_evaluaciones": vista_formulario.fecha_fin_evaluaciones,
            "duracion_semanas": vista_formulario.duracion_semanas_entry.get(),
            "estado": dic_estado.get(vista_formulario.var_estado.get(),"planificacion"),
            "observaciones": vista_formulario.observacion_entry.get()
        }
        return datos_periodo
    
    def obtener_nombres_periodos(self):
        dic_periodos = self.modelo_pa.obtener_periodos_academicos()
        return [periodo["nombre"] for periodo in dic_periodos]
    
    #================================================================================================================================================================================
    
    def obtener_periodos_academicos(self):
        """Retorna todos los periodos académicos completos como lista de dicts."""
        return self.modelo_pa.obtener_periodos_academicos()

    def actualizar_periodo_academico(self, id_periodo, datos_actualizados, ventana):
        resultado = self.modelo_pa.actualizar_periodo_academico(id_periodo, datos_actualizados)
        if resultado:
            messagebox.showinfo("Actualización exitosa", "El período académico ha sido actualizado correctamente.", parent=ventana)
            return True
        else:
            messagebox.showerror("Error", "No se pudo actualizar el período académico.", parent=ventana)
            return False

    
