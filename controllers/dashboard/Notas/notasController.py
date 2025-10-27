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
        notas = self.modelo_notas.listar_notas_estudiante(estudiante_id)
        print("Notas obtenidas:", notas)  # Para depuración
        asistencias = self.modelo_notas.obtener_historial_asistencias(estudiante_id)

        # Crear un diccionario para mapear inscripcion_id a asistencia
        mapeo = {}
        for a in asistencias:
            insc = a.get("inscripcion_id")
            if insc is not None:
                mapeo[insc] = a
            
        coincidencias = []
        trayecto_promedios = {}  # Para almacenar promedios por trayecto
        for nota in notas:
            trayecto_id = nota.get("trayecto_id")
            valor_nota = nota.get("valor")

            if trayecto_id not in trayecto_promedios:
                trayecto_promedios[trayecto_id] = {"total": 0, "count": 0}
            
            if valor_nota is not None:
                trayecto_promedios[trayecto_id]["total"] += valor_nota
                trayecto_promedios[trayecto_id]["count"] += 1

        # Calcular promedios finales y agregar a coincidencias
        for trayecto_id, datos in trayecto_promedios.items():
            if datos["count"] > 0:
                promedio = datos["total"] / datos["count"]
                coincidencias.append({"trayecto_id": trayecto_id, "promedio": promedio})
        return coincidencias

    def obtener_historial_academico_completo(self, estudiante_id):
        notas = self.modelo_notas.listar_notas_estudiante(estudiante_id)
        print("Notas obtenidas:", notas)  # Para depuración

        # Crear un diccionario para almacenar las notas por trayecto y tramo
        trayecto_tramo_map = {}

        for nota in notas:
            trayecto_id = nota.get("trayecto_id")
            tramo = nota.get("tramo")
            valor_nota = nota.get("valor")

            # Solo considerar una nota por unidad curricular por trayecto
            if trayecto_id not in trayecto_tramo_map:
                trayecto_tramo_map[trayecto_id] = {}

            if tramo not in trayecto_tramo_map[trayecto_id]:
                trayecto_tramo_map[trayecto_id][tramo] = []

            # Agregar la nota al tramo correspondiente solo si no existe ya
            if valor_nota is not None and valor_nota not in trayecto_tramo_map[trayecto_id][tramo]:
                trayecto_tramo_map[trayecto_id][tramo].append(valor_nota)

        # Calcular promedios finales y crear la lista de resultados
        coincidencias = []
        for trayecto_id, tramos in trayecto_tramo_map.items():
            for tramo, notas in tramos.items():
                if notas:  # Solo si hay notas
                    promedio = sum(notas) / len(notas)
                    coincidencias.append({
                        "trayecto_id": trayecto_id,
                        "tramo": tramo,
                        "promedio": promedio
                    })

        return coincidencias
