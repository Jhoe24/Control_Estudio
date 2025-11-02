from pathlib import Path
import sqlite3 as sql
import os
from datetime import date, datetime
import pandas as pd

class ModeloExportar:
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')

        self.tablas_exportables = {
            "informacion_personal": "Información Personal",
            "telefonos": "Teléfonos",
            "direcciones": "Direcciones",
            "estudiantes": "Estudiantes",
            "estudiante_pnf": "Estudiantes PNF",
            "docentes": "Docentes",
            "sedes": "Sedes",
            "docente_sede_pnf": "Docentes Sede PNF",
            "pnf": "PNFs",
            "trayectos": "Trayectos",
            "tramos": "Tramos",
            "unidades_curriculares": "Unidades Curriculares",
            "docente_uc": "Docente UC",
            "periodos_academicos": "Períodos",
            "secciones": "Secciones",
            "inscripciones": "Inscripciones",
            "notas": "Notas",
            "asistencia": "Asistencias",
        }

        self.nombre_tabla_exportable = list(self.tablas_exportables.keys())#Obtener la lista de tablas exportables
        self.valores_tabla = list(self.tablas_exportables.values())#Obtener la lista de valores de las tablas exportables
        
    def __obtener_informacion(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            for tabla in self.nombre_tabla_exportable:
                cursor.execute(f"SELECT * FROM {tabla}")
                resultado = cursor.fetchall()
                columnas = [descripcion[0] for descripcion in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                yield tabla, df
           
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}") 
            # En un generador, es mejor no devolver nada o lanzar la excepción.
            # Un return vacío detiene la iteración.
        finally:
            # La conexión se debe cerrar aquí para asegurar que se cierre al final.
            if con is not None:
                con.close()

    def exportar_a_excel(self, ruta_archivo=None, progress_callback=None):
        """
        Exporta los datos de todas las tablas definidas en `tablas_exportables`
        a un único archivo de Excel, con una hoja por tabla.

        Args:
            ruta_archivo (str, optional): La ruta completa donde se guardará el archivo Excel.
                                          Si es None, se guardará en una carpeta por defecto
                                          en los Documentos del usuario.
            progress_callback (function, optional): Una función a la que se llamará después de
                                                    exportar cada tabla. Recibe (items_procesados, total_items).

        Returns:
            str|None: La ruta del archivo si la exportación fue exitosa, None en caso contrario.
        """
        try:
            if not ruta_archivo:
                # Lógica para crear una ruta por defecto si no se proporciona una.
                documents_path = Path.home() / "Documents"

                if not documents_path.exists():
                    documents_path = Path.home() / "Documentos" # Fallback para Windows en español

                # Usar un nombre de carpeta más apropiado
                export_dir = documents_path / "Exportaciones del Sistema"
                export_dir.mkdir(parents=True, exist_ok=True)
                
                # Nombre de archivo con fecha y hora para evitar sobreescrituras
                nombre_archivo = f"exportacion_completa_{date.today().strftime('%Y%m%d')}.xlsx"
                ruta_archivo = export_dir / nombre_archivo

            total_tablas = len(self.nombre_tabla_exportable)
            tablas_exportadas = 0

            # --- INICIO DE LA MODIFICACIÓN ---
            # Definir los metadatos personalizados que se añadirán al archivo
            identificador_sistema = "CONTROL-ESTUDIO-V1"
            fecha_exportacion = datetime.now().isoformat()
            
            # --- FIN DE LA MODIFICACIÓN ---

            with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                for tabla, df in self.__obtener_informacion():
                    # Usar el nombre "amigable" de la tabla como nombre de la hoja
                    nombre_hoja = self.tablas_exportables.get(tabla, tabla)
                    print(f"Exportando tabla '{tabla}' a la hoja '{nombre_hoja}'...")
                    df.to_excel(writer, sheet_name=nombre_hoja, index=False)

                    # Notificar el progreso si hay un callback
                    tablas_exportadas += 1
                    if progress_callback:
                        progress_callback(tablas_exportadas, total_tablas)
                
                # --- INICIO DE LA MODIFICACIÓN ---
                # Acceder al objeto workbook de openpyxl y añadir las propiedades
                workbook = writer.book
                workbook.custom_doc_props.system_id = identificador_sistema
                workbook.custom_doc_props.export_date = fecha_exportacion
                # --- FIN DE LA MODIFICACIÓN ---
            
            print(f"Exportación completada exitosamente. Archivo guardado en: {ruta_archivo}")
            return str(ruta_archivo) # Devolver la ruta en caso de éxito
        except Exception as e:
            print(f"Error al exportar a Excel: {e}")
            return None # Devolver None en caso de error
        
    def exportarSQL(self, directorio_destino, progress_callback=None):
        """
        Exporta la base de datos a un archivo .sql en el directorio especificado.

        Args:
            directorio_destino (str): La carpeta donde se guardará el archivo SQL.
            progress_callback (function, optional): Callback para notificar el progreso.
                                                    Recibe (items_procesados, total_items).
        Returns:
            str|None: La ruta del archivo si la exportación fue exitosa, None en caso contrario.
        """
        con = None
        try:
            # 1. Asegurarse de que el directorio de destino exista
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)
                print(f"Directorio creado: {directorio_destino}")
            
            nombre_archivo_sql = f"respaldo_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            sql_dump_file = os.path.join(directorio_destino, nombre_archivo_sql)

            con = sql.connect(self.db_ruta)
            
            # Contar tablas para la barra de progreso
            total_tablas = len(self.nombre_tabla_exportable)
            tablas_exportadas = 0
            
            # 2. Abrir el archivo de salida para escribir
            with open(sql_dump_file, 'w') as f:
                print(f"Exportando base de datos a: '{sql_dump_file}'...")
                
                # 3. Iterar sobre las líneas de SQL generadas por iterdump()
                for line in con.iterdump():
                    f.write(f'{line}\n')
                    # Si la línea es un COMMIT, consideramos que una tabla ha terminado.
                    if 'COMMIT' in line and progress_callback:
                        tablas_exportadas += 1
                        progress_callback(tablas_exportadas, total_tablas)
            
            print("¡Exportación SQL completada exitosamente!")
            return sql_dump_file
        except Exception as e:
            print(f"Error durante la exportación SQL: {e}")
            return None
        finally:
            if con:
                con.close()