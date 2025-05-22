# archivo migrador_base.py
import os
import sys
import sqlite3
import pandas as pd
import logging
import datetime
import re
from tkinter import Tk, filedialog
from typing import Tuple, List, Dict, Any, Optional

# Crear directorio de logs si no existe
if not os.path.exists('logg'):
    os.makedirs('logg')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logg/migracion_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("migracion")

class MigradorBase:
    """
    Clase base para manejar la migración de datos desde archivos Excel a una base de datos SQLite3.
    """

    def __init__(self, db_path: str):
        """
        Inicializa el migrador con la ruta a la base de datos SQLite3.

        Args:
            db_path: Ruta al archivo de la base de datos SQLite3
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.df_data = None
        self.conteo_migraciones = {}
        self.total_registros = 0
        
        self.registros_actualizados = {}
        self.registros_cedula_vacia = {}
        self.registros_cedula_invalida = {}

    def conectar_db(self) -> bool:
        """
        Establece conexión con la base de datos SQLite3.

        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
            logger.info(f"Conexión exitosa a la base de datos: {self.db_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            return False

    def cerrar_db(self) -> None:
        """Cierra la conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            logger.info("Conexión a la base de datos cerrada")

    def seleccionar_archivo_excel(self) -> str:
        """
        Abre un diálogo para seleccionar un archivo Excel.

        Returns:
            str: Ruta al archivo seleccionado o cadena vacía si se cancela
        """
        try:
            root = Tk()
            root.withdraw()  # Ocultar la ventana principal
            root.attributes('-topmost', True)  # Poner ventana al frente
            
            file_path = filedialog.askopenfilename(
                title="Seleccione el archivo Excel con los datos",
                filetypes=[
                    ("Archivos Excel", "*.xlsx"),
                    ("Archivos Excel (legacy)", "*.xls"),
                    ("Todos los archivos", "*.*")
                ]
            )
            root.destroy()
            
            if file_path:
                logger.info(f"Archivo seleccionado: {file_path}")
            else:
                logger.warning("No se seleccionó ningún archivo")
                
            return file_path
        except Exception as e:
            logger.error(f"Error al seleccionar archivo: {e}")
            return ""

    def cargar_datos_excel(self, file_path: str, columnas_requeridas: List[str] = None) -> bool:
        """
        Carga datos desde un archivo Excel.

        Args:
            file_path: Ruta al archivo Excel
            columnas_requeridas: Lista de columnas requeridas en el archivo Excel

        Returns:
            bool: True si la carga fue exitosa, False en caso contrario
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                logger.error(f"El archivo no existe: {file_path}")
                return False

            # Cargar el archivo Excel
            logger.info(f"Cargando datos desde: {file_path}")
            self.df_data = pd.read_excel(file_path)

            # Verificar que se hayan cargado datos
            if self.df_data.empty:
                logger.error("El archivo Excel no contiene datos")
                return False

            logger.info(f"Columnas encontradas en el archivo: {list(self.df_data.columns)}")

            # Verificar que las columnas necesarias estén presentes
            if columnas_requeridas:
                columnas_faltantes = [col for col in columnas_requeridas if col not in self.df_data.columns]
                if columnas_faltantes:
                    logger.error(f"Faltan columnas requeridas en el archivo Excel: {columnas_faltantes}")
                    logger.error(f"Columnas disponibles: {list(self.df_data.columns)}")
                    return False

            # Limpiar valores NaN y espacios en blanco
            self.df_data = self.df_data.fillna('')
            for col in self.df_data.columns:
                if self.df_data[col].dtype == 'object':
                    self.df_data[col] = self.df_data[col].astype(str).str.strip()

            self.total_registros = len(self.df_data)
            logger.info(f"Datos cargados exitosamente. Total de registros: {self.total_registros}")
            return True

        except Exception as e:
            logger.error(f"Error al cargar datos desde Excel: {e}")
            return False

    def _validar_cedula(self, valor):
        """Valida y limpia el número de cédula"""
        if pd.isna(valor):
            return None
        cedula = str(valor).strip()
        if not cedula or cedula.lower() in ['nan', 'none', 'null', '']:
            return None
        # Remover caracteres no numéricos excepto guiones
        cedula = re.sub(r'[^\d-]', '', cedula)
        
        # Verificar si la cédula tiene solo un dígito (inválida)
        if cedula and len(cedula.replace('-', '')) == 1:
            return "CEDULA_UN_DIGITO"  # Marcador especial
        
        return cedula if cedula else None

    def _formatear_tipo_documento(self, valor):
        """Formatea el tipo de documento"""
        if pd.isna(valor):
            return 'cedula'
        val = str(valor).strip().lower()
        if val in ['v', 'verdadero', 'true', '1']:
            return 'extranjero'
        if val in ['f', 'falso', 'false', '0', '']:
            return 'cedula'
        return 'cedula'

    def _formatear_fecha(self, fecha_str: Any) -> Optional[str]:
        """Formatea fechas a formato YYYY-MM-DD"""
        # Manejar valores nulos o NaT de pandas
        if pd.isna(fecha_str) or fecha_str == '' or str(fecha_str).strip() == '':
            return None
            
        # Si es objeto datetime o Timestamp
        if isinstance(fecha_str, (datetime.date, datetime.datetime, pd.Timestamp)):
            try:
                return fecha_str.strftime('%Y-%m-%d')
            except Exception:
                return None
                
        # Intentar formatos con posible componente horario
        formatos = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']
        for fmt in formatos:
            try:
                fecha = datetime.datetime.strptime(str(fecha_str), fmt)
                return fecha.strftime('%Y-%m-%d')
            except ValueError:
                continue
                
        logger.warning(f"No se pudo formatear la fecha: {fecha_str}")
        return None

    def _formatear_nacionalidad(self, valor):
        """Formatea la nacionalidad"""
        if pd.isna(valor) or not str(valor).strip():
            return "Otro"
        val = str(valor).strip().lower()
        if val in ["v", "venezolano", "venezolana"]:
            return "Venezolano"
        if val in ["e", "extranjero", "extrangero"]:
            return "Extranjero"
        return val.capitalize()

    def _formatear_telefono(self, telefono: str) -> Tuple[str, str]:
        """
        Formatea un número de teléfono separando el código de área y el número.
        Maneja números venezolanos en diferentes formatos.

        Args:
            telefono: Número de teléfono en diferentes formatos

        Returns:
            Tuple[str, str]: (código_area, número) - Retorna ('', '') si es inválido
        """
        if pd.isna(telefono) or not str(telefono).strip():
            return '', ''

        telefono_str = str(telefono).strip()
        
        # Si está vacío después del strip
        if not telefono_str:
            return '', ''

        # Códigos de área válidos para Venezuela (móviles y fijos)
        codigos_moviles = ['0412', '0414', '0416', '0426', '0424']
        codigos_fijos = ['0212', '0241', '0243', '0245', '0251', '0261', '0264', '0271', '0272', '0273', '0274', '0275', '0276', '0281', '0285', '0287', '0288', '0291', '0295']
        codigos_area_validos = codigos_moviles + codigos_fijos

        # Limpiar caracteres no numéricos excepto paréntesis y guiones
        telefono_limpio = re.sub(r'[^\d()-]', '', telefono_str)
        
        # Caso 1: Formato (0414)1542451
        match = re.search(r'\((\d{4})\)(\d{7})', telefono_limpio)
        if match:
            codigo_area = match.group(1)
            numero = match.group(2)
            if codigo_area in codigos_area_validos:
                return codigo_area, numero
        
        # Caso 2: Formato (414)1542451 (sin el 0 inicial)
        match = re.search(r'\((\d{3})\)(\d{7})', telefono_limpio)
        if match:
            codigo_area = '0' + match.group(1)  # Agregar el 0
            numero = match.group(2)
            if codigo_area in codigos_area_validos:
                return codigo_area, numero
        
        # Caso 3: Formato 0414-2548547 (con guión después del código de área completo)
        match = re.search(r'^(\d{4})-(\d{7})$', telefono_limpio)
        if match:
            codigo_area = match.group(1)
            numero = match.group(2)
            if codigo_area in codigos_area_validos:
                return codigo_area, numero
        
        # Caso 4: Formato 412-5548253 (sin el 0 inicial y con guión)
        match = re.search(r'^(\d{3})-(\d{7})$', telefono_limpio)
        if match:
            codigo_area = '0' + match.group(1)  # Agregar el 0
            numero = match.group(2)
            if codigo_area in codigos_area_validos:
                return codigo_area, numero
        
        # Caso 5: Formato 04125478745 (11 dígitos)
        if len(telefono_limpio) == 11 and telefono_limpio.startswith('0'):
            codigo_area = telefono_limpio[:4]
            numero = telefono_limpio[4:]
            if codigo_area in codigos_area_validos:
                return codigo_area, numero
        
        # Caso 6: Formato 4247412365 (10 dígitos, sin el 0 inicial)
        if len(telefono_limpio) == 10:
            codigo_area_sin_cero = telefono_limpio[:3]
            codigo_area = '0' + codigo_area_sin_cero
            numero = telefono_limpio[3:]
            if codigo_area in codigos_area_validos:
                return codigo_area, numero
        
        # Caso 7: Formato 02735548965 (11 dígitos, teléfono fijo)
        if len(telefono_limpio) == 11 and telefono_limpio.startswith('0'):
            # Probar con código de 4 dígitos primero
            codigo_area = telefono_limpio[:4]
            numero = telefono_limpio[4:]
            if codigo_area in codigos_area_validos and len(numero) == 7:
                return codigo_area, numero
        
        # Si no coincide con ningún patrón válido, retornar vacío
        logger.warning(f"Formato de teléfono no reconocido o inválido: {telefono_str}")
        return '', ''

    def _validar_correo(self, correo: str) -> bool:
        """
        Valida el formato de un correo electrónico.

        Args:
            correo: Correo electrónico a validar

        Returns:
            bool: True si el correo es válido, False en caso contrario
        """
        if pd.isna(correo) or not str(correo).strip():
            return False

        correo_str = str(correo).strip()
        # Expresión regular para validar el formato de un correo electrónico
        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron_correo, correo_str) is not None

    def _formatear_sexo(self, sexo: Any) -> Optional[str]:
        """Formatea el sexo a M o F"""
        # Manejar valores nulos
        if pd.isna(sexo) or str(sexo).strip() == '':
            return None
        s = str(sexo).strip().lower()
        if s in ['verdadero', 'true', '1', 'v', 'm', 'masculino', 'hombre']:
            return 'M'
        if s in ['falso', 'false', '0', 'f', 'femenino', 'mujer']:
            return 'F'
        logger.warning(f"Sexo no reconocido: {sexo}")
        return None

    def _formatear_estado_civil(self, estado: Any) -> Optional[str]:
        """
        Normaliza el estado civil a uno de los valores permitidos:
        ('Soltero', 'Casado', 'Divorciado', 'Viudo', 'Otro').
        """
        if pd.isna(estado) or not str(estado).strip():
            return None
        e = str(estado).strip().lower()
        if e in ['soltero', 'soltera', 'single']:
            return 'Soltero'
        if e in ['casado', 'casada', 'married']:
            return 'Casado'
        if e in ['divorciado', 'divorciada', 'divorced']:
            return 'Divorciado'
        if e in ['viudo', 'viuda', 'widowed']:
            return 'Viudo'
        # Cualquier otro caso
        return 'Otro'

    def ejecutar_migracion(self, columnas_requeridas: List[str] = None) -> Tuple[bool, Dict[str, int]]:
        """
        Ejecuta el proceso completo de migración.

        Args:
            columnas_requeridas: Lista de columnas requeridas en el archivo Excel

        Returns:
            Tuple[bool, Dict[str, int]]: (éxito, conteo de registros migrados por tabla)
        """
        exito = True

        # Conectar a la base de datos
        if not self.conectar_db():
            return False, self.conteo_migraciones

        try:
            # Seleccionar y cargar archivo Excel
            print("\nSeleccione el archivo Excel con los datos a migrar...")
            archivo_excel = self.seleccionar_archivo_excel()
            if not archivo_excel:
                logger.warning("No se seleccionó ningún archivo. Operación cancelada.")
                return False, self.conteo_migraciones

            if not self.cargar_datos_excel(archivo_excel, columnas_requeridas):
                return False, self.conteo_migraciones

            # Iniciar transacción para toda la migración
            self.conn.execute("BEGIN TRANSACTION")

            # Ejecutar migración por etapas
            if not self.migrar_informacion_personal():
                self.conn.rollback()
                exito = False
            elif not self.migrar_telefonos():
                self.conn.rollback()
                exito = False
            elif not self.migrar_direcciones():
                self.conn.rollback()
                exito = False
            elif not self.migrar_especifico():
                self.conn.rollback()
                exito = False
            else:
                # Si todo salió bien, confirmar los cambios
                self.conn.commit()
                logger.info("Migración completada exitosamente")

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error durante la migración: {e}")
            exito = False

        finally:
            # Cerrar conexión a la base de datos
            self.cerrar_db()

        return exito, self.conteo_migraciones

    def migrar_informacion_personal(self) -> bool:
        """
        Migra la información personal a la tabla informacion_personal.

        Returns:
            bool: True si la migración fue exitosa, False en caso contrario
        """
        pass

    def migrar_telefonos(self) -> bool:
        """
        Migra la información de teléfonos a la tabla telefonos.

        Returns:
            bool: True si la migración fue exitosa, False en caso contrario
        """
        pass

    def migrar_direcciones(self) -> bool:
        """
        Migra la información de direcciones a la tabla direcciones.

        Returns:
            bool: True si la migración fue exitosa, False en caso contrario
        """
        pass

    def migrar_especifico(self) -> bool:
        """
        Migra la información específica a la tabla correspondiente.

        Returns:
            bool: True si la migración debe ser implementado por la clase hija, False en caso contrario
        """
        pass

