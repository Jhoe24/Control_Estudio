import os
from datetime import datetime
from docxtpl import DocxTemplate
from pathlib import Path
try:
    from docx2pdf import convert
except ImportError:
    convert = None

class ModelSolicitud:
    def __init__(self):
        self.datos = None
        self.output_path = "reportes/constancias"
        self.template_path = "reportes/plantillas/plantilla_constancia.docx"
        self.pdf_output_path = "reportes/constancias/pdf"
        os.makedirs(self.output_path, exist_ok=True)

    def generar_docx(self, datos):
        """
        Genera el archivo DOCX de la constancia de estudio a partir de una plantilla.
        """
        self.datos = datos
        try:
            doc = DocxTemplate(self.template_path)
        except Exception as e:
            print(f"Error al cargar la plantilla: No se pudo encontrar en '{self.template_path}'. Detalles: {e}")
            return None # Devolver None si la plantilla no se encuentra

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
            'coordinador': "________________________",
            'cedula_coordinador': "________________",
            'cargo_coordinador': "COORDINADOR(A) DE CONTROL DE ESTUDIOS",
            'correo_contacto': "correo: ___________________"
        }

        doc.render(context)

        # Guardar el documento generado
        filename = f"constancia_{self.datos['documento_identidad']}_{now.strftime('%Y%m%d%H%M%S')}.docx"
        filepath = os.path.join(self.output_path, filename)
        doc.save(filepath)
        return filepath
    
    def convertir_a_pdf(self, ruta_docx):
        """
        Convierte un archivo DOCX a PDF.
        """
        if convert is None:
            print("Error: La librería 'docx2pdf' no está instalada. Ejecuta 'pip install docx2pdf'.")
            return None

        if not os.path.exists(ruta_docx):
            print(f"Error: El archivo DOCX no se encuentra en '{ruta_docx}'")
            return None

        try:
            # Obtener la ruta de la carpeta "Documentos" del usuario
            # Path.home() encuentra el directorio de inicio del usuario (ej: C:\Users\TuUsuario)
            documents_path = Path.home() / "Documents"

            # Si la carpeta "Documents" no existe, intenta con "Documentos" (para Windows en español)
            if not documents_path.exists():
                documents_path = Path.home() / "Documentos"

            # Crear una subcarpeta para las constancias si no existe
            pdf_output_dir = documents_path / "Constancias de Estudio"
            pdf_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Convertir el archivo y guardarlo en la nueva ruta
            ruta_pdf_final = pdf_output_dir / Path(ruta_docx).name.replace('.docx', '.pdf')
            convert(ruta_docx, str(ruta_pdf_final))
            
            print(f"Archivo convertido a PDF exitosamente en: {ruta_pdf_final}")
            return str(ruta_pdf_final)
        except Exception as e:
            print(f"Error al convertir a PDF. Asegúrate de que Microsoft Word esté instalado. Detalles: {e}")
            return None