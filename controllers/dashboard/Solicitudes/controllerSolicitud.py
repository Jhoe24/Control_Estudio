from models.Solicitudes.modelSolicitud import ModelSolicitud

class ControllerSolcitud:
    def __init__(self):
        self.model = ModelSolicitud()

    def generar_constancia(self, datos):
        return self.model.generar_docx(datos)
    
    def convertir_a_pdf(self, ruta_docx):
        return self.model.convertir_a_pdf(ruta_docx)