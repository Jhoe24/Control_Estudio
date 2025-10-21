from models.Solicitudes.modelSolicitud import ModelSolicitud
from models.Solicitudes.modeloSituacionAcademica import ModeloSituacionAcademica

class ControllerSolcitud:
    def __init__(self):
        self.model = ModelSolicitud()
        

    def generar_constancia(self, datos):
        return self.model.generar_docx(datos)
    
    def convertir_a_pdf(self, ruta_docx):
        return self.model.convertir_a_pdf(ruta_docx)
    
    def generarSituacionAcademica(self, datosEstudiante, listNotas):
        try:
            return ModeloSituacionAcademica(datosEstudiante=datosEstudiante, listNotas=listNotas) 
        except Exception as e:
            print(f"Error al generar Situación Académica: {e}")
            return None
        
    