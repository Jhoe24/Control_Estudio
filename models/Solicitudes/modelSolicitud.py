import os
from datetime import datetime
from docxtpl import DocxTemplate

class ModelSolicitud:
    def __init__(self):
        self.datos = None
        self.output_path = "reportes/constancias"
        self.template_path = "reportes/plantillas/plantilla_constancia.docx"
        os.makedirs(self.output_path, exist_ok=True)

    def generar_docx(self, datos):
        """
        Genera el archivo DOCX de la constancia de estudio a partir de una plantilla.
        """
        self.datos = datos
        try:
            doc = DocxTemplate(self.template_path)
        except Exception as e:
            print(f"Error: No se pudo encontrar la plantilla en '{self.template_path}'. Asegúrate de que el archivo existe.")
            raise e

        now = datetime.now()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        # Mapeo de sexo a texto
        sexo_map = {'M': 'el ciudadano', 'F': 'la ciudadana'}
        sexo_texto = sexo_map.get(self.datos.get('sexo', 'M'), 'el/la ciudadano(a)')

        context = {
            'sexo': sexo_texto,
            'nombre_estudiante': f"{self.datos.get('nombres', '')} {self.datos.get('apellidos', '')}".upper(),
            'tipo_documento': self.datos.get('tipo_documento', 'C.I.'),
            'numero_documento': self.datos.get('documento_identidad', 'N/A'),
            'nombre_trayecto': self.datos.get('trayecto_nombre', 'N/A').upper(),
            'pnf_nombre': self.datos.get('pnf_nombre', 'N/A').upper(),
            'periodo_academico': self.datos.get('periodo_academico_nombre', 'Actual').upper(),
            'sede': self.datos.get('sede_nombre', 'Barinas').upper(),
            'fecha': f"{now.day} de {meses[now.month - 1]} de {now.year}",
            
            # Datos del coordinador (puedes moverlos a un archivo de configuración)
            'coordinador': "ING. JOSÉ AGUSTÍN PÉREZ",
            'cedula_coordinador': "V-12.345.678",
            'cargo_coordinador': "COORDINADOR(A) DE CONTROL DE ESTUDIOS",
            'correo_contacto': "dacecg@gmail.com"
        }

        doc.render(context)

        # Guardar el documento generado
        filename = f"constancia_{self.datos['documento_identidad']}_{now.strftime('%Y%m%d%H%M%S')}.docx"
        filepath = os.path.join(self.output_path, filename)
        doc.save(filepath)
        return filepath

