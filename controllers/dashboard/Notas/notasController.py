from models.Notas.modelNotas import ModeloNotas
from models.PNF.modelo_pnf import ModeloPNF
import tkinter.messagebox as messagebox

class NotasController:
    def __init__(self):
        self.modelo_notas = ModeloNotas()
        self.modelo_pnf = ModeloPNF()
    
    def validate_project(self, estudiante_id, vistaMostrar):
        """
        Valida si un estudiante ha aprobado la unidad curricular de "Proyecto"
        según las notas registradas en su trayecto actual.
        """
        pnfActualInfo = self.modelo_notas.is_assigned_pnf(estudiante_id)

        if not pnfActualInfo:
            messagebox.showerror("Error de Asignación", "El estudiante no está asignado a ningún P.N.F.", parent=vistaMostrar)
            return False
        
        pnf_id, trayectoActual  = pnfActualInfo
        trayectoId = self.modelo_pnf.obtener_id_por_nombre_y_pnf("trayectos", trayectoActual, pnf_id)
    
        if not trayectoId:
            mensaje = f"No se pudo encontrar el ID para el trayecto '{trayectoActual}' en el PNF actual."
            messagebox.showerror("Error de Datos", mensaje, parent=vistaMostrar)
            return False
        
        """ Verificar que el trayecto no sea el inicial para que se cumpla con la validacion"""
        if self.modelo_notas.esTrayectoInicial(trayectoId):
            return True
        
        lisDicNotasEstudiante  = self.modelo_notas.bring_project(estudiante_id,pnf_id,trayectoId)
        

        if not lisDicNotasEstudiante:
            mensaje = "No se encontró la materia 'Proyecto' para el trayecto actual del estudiante o no tiene notas cargadas."
            messagebox.showwarning("Sin Notas", mensaje, parent=vistaMostrar)
            return False
        numero_uc = len(lisDicNotasEstudiante)
        # Filtrar solo las notas que no son None y convertirlas a entero
       
        conNotas = 0.0
        for dicNotas in lisDicNotasEstudiante:
            if dicNotas["nota"]:
                conNotas = conNotas + dicNotas["nota"]
        
        if conNotas == 0.0:
            messagebox.showwarning("Sin Notas Válidas", "El estudiante no tiene notas válidas cargadas en la materia de Proyecto.", parent=vistaMostrar)
            return False
            
        """
        Segun el documento rector: Para aprobar la unidad curricular de proyecto se necesita que sea 
        mayor o igual a 16
        """
        nota_final = conNotas // numero_uc
        # print("Notas Final: ",nota_final)
        # print("ConNotas: ", conNotas)
        # print("numero de uc: ", numero_uc)
        if nota_final >= 16:
            return True
        else:
            mensaje = f"El estudiante no ha aprobado la materia de Proyecto.\nSu nota final es de: {nota_final}"
            messagebox.showwarning("No Aprobado", mensaje, parent=vistaMostrar)
            return False
        
    def estudiantes_por_uc(self, unidad_curricular_id, periodo_academico_id):
        return self.modelo_notas.estudiantes_por_uc(unidad_curricular_id, periodo_academico_id)
    
    def listarNotasEstudiante(self, estudiante_id):
        return self.modelo_notas.listar_notas_estudiante(estudiante_id)
    
    def obtener_historial_asistencias(self, estudiante_id):
        return self.modelo_notas.obtener_historial_asistencias(estudiante_id)
    
    def obtener_lista_notas_historialAcademico(self, estudiante_id):
        dic = []
        notas = self.modelo_notas.listar_notas_estudiante(estudiante_id)
        asistencias = self.modelo_notas.obtener_historial_asistencias(estudiante_id)

        # Crear un diccionario para mapear inscripcion_id a asistencia
        mapeo = {}
        for a in asistencias:
            insc = a.get("inscripcion_id")
            if insc is not None:
                mapeo[insc] = a
            
        coincidencias = []
        for n in notas:
            insc = n.get("inscripcion_id")
            if insc is None:
                continue
            if insc in mapeo:
                combinado = n.copy()  # Copiar los datos de la nota
                combinado["asistencia"] = mapeo[insc].get("asistencia")  # Agregar la asistencia correspondiente
                coincidencias.append(combinado)

        return coincidencias



