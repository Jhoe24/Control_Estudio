from pathlib import Path


class ModeloSituacionAcademica:
    def __init__(self, datosEstudiante, listNotas):
        self.datosEstudiante = datosEstudiante
        self.listNotas = listNotas
        self._fuente = "Arial"

        documents_path = Path.home() / "Documents"
            # Si la carpeta "Documents" no existe, intenta con "Documentos" (para Windows en español)
        if not documents_path.exists():
            documents_path = Path.home() / "Documentos"

        # Crear una subcarpeta para las constancias si no existe
        pdf_output_dir = documents_path / "Situaciones Academicas"
        pdf_output_dir.mkdir(parents=True, exist_ok=True)
        self._rutaFinal = pdf_output_dir 
        self._nombreArchivo = f"Situacion_Academica_{datosEstudiante['cedula']}.pdf"

        self._imgLogo = "resources\images\logo4.jpg"

        self._cabeceraIzquierda = {"texto":"""REPUBLICA BOLIVARIANA DE VENEZUELA
                                UNIVERSIDAD POLITECNICA TERRITORIAL
                                DEL ESTADO BARINAS
                                "JOSÉ FÉLIX RIBAS"
                                R.I.F.: G-20009502-4
                                  """,
                                "tamanoFuente":16}
        
        self._cabeceraDerecha = {"texto":f"""SECRETARIA GENERAL
                                 Coordinación de Admisión, Seguimiento, Registro y Control de Estudio
                                 Núcleo {datosEstudiante['nucleo']}
                                  """,
                                "tamanoFuente":12}
        
        self._titulo = {"texto":"SITUACION ACADEMICA",
                        "tamanoFuente":25}
        
        self._datosPrimeraTabla = [
            {"etiqueta":"Documento de Identidad:", "valor":datosEstudiante['cedula']},
            {"etiqueta":"Apellidos y Nombres:", "valor":datosEstudiante['nombres']},
            {"etiqueta":"Cursando:", "valor":datosEstudiante['pnf']},
            {"etiqueta":"Indice Académico Acumulado::", "valor":datosEstudiante['indiceAcademico']},
        ]
        # De esta manera se va a organizar la tabla de notas
        self._cabecera_tabla_notas =["Año","trayecto", "Unidad Curricular Cursada", "Nota", "Asist", "U.C", "Condicion"]

        # Datos despues de la tabla de notas
        self._firmaCoordinador = {
            "texto":f"\n\n\n\n\n__________________________\nLcdo. Henry Rujano Herrera\nV-14002390\nCoordinador de Admisión, Seguimiento, Registro y Control de Estudio Núcleo {self.datosEstudiante['nucleo']}",
            "tamanoFuente":12
        }

        #Pie de pagina
        self._tituloPiePagina = "Tecnología al Servicio de la Comunidad"#<-- Texto centrado y en negreita y tamaño 12
        
        # esta tabla debe ser de 1X4
        self.tablaPiepagina = {
            "1X1":"Extension Barinas\nAv. Industrial Frente al Aserradero El Pozon\n(0273)5413579 - (0273)5413657",
            "1X2":"Núcleo Barinitas\nNúcleo Barinitas\nNúcleo Barinitas",
            "1X3":"Núcleo Socopó\nCarrera 7 Vía El Uno\n(0273)8718535",
            "1X4":"Extensión Pedraza\nHacienda Ticoporo, Ciudad Bolivia\n(0273)9210269"
        }
    def generarPdf(self):
        # Lógica para generar el PDF utilizando self.datosEstudiante y self.listNotas
        pass