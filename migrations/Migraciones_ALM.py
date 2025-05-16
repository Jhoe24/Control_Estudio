"""
Script para migrar datos de la tabla ALM desde archivos Excel a una nueva estructura SQLite3.

Este script:
1. Permite seleccionar y cargar datos de archivos Excel que contienen la tabla ALM
2. Valida los datos para asegurar su integridad
3. Migra los datos a la nueva estructura de la base de datos SQLite3
4. Registra el proceso de migración y cualquier error encontrado
"""

import os
import sys
import sqlite3
import pandas as pd
import logging
import datetime
import re
from tkinter import Tk, filedialog
from typing import Tuple, List, Dict, Any, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logg/migracion_alm_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
    
)
logger = logging.getLogger("migracion_alm")

class MigradorALM:
    """
    Clase para manejar la migración de datos de la tabla ALM a la nueva estructura SQLite3.
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
        self.df_alm = None
        self.conteo_migraciones = {
            "personal": 0,
            "telefonos": 0,
            "direcciones": 0,
            "estudiantes": 0
        }
        self.total_registros = 0
    
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
        root = Tk()
        root.withdraw()  # Ocultar la ventana principal
        file_path = filedialog.askopenfilename(
            title="Seleccione el archivo Excel con los datos de ALM",
            filetypes=[("Archivos Excel", "*.xlsx;*.xls")]
        )
        root.destroy()
        return file_path
    
    def cargar_datos_excel(self, file_path: str) -> bool:
        """
        Carga datos desde un archivo Excel.
        
        Args:
            file_path: Ruta al archivo Excel
            
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario
        """
        try:
            # Cargar el archivo Excel
            logger.info(f"Cargando datos desde: {file_path}")
            self.df_alm = pd.read_excel(file_path)
            
            # Verificar que se hayan cargado datos
            if self.df_alm.empty:
                logger.error("El archivo Excel no contiene datos")
                return False
            
            # Verificar que las columnas necesarias estén presentes
            columnas_requeridas = [
                'A_ID', 'A_NOMBRE', 'A_APELLIDO', 'A_FINGRESO', 'A_FNACIMIE', 
                'A_SEXO', 'A_ECIVIL', 'A_NACIONAL', 'A_LNACIMIE', 'A_TEL1', 
                'A_TEL2', 'A_TEL3', 'A_EDORESID', 'A_MUNRESID', 'A_DIRECCIO'
            ]
            
            columnas_faltantes = [col for col in columnas_requeridas if col not in self.df_alm.columns]
            if columnas_faltantes:
                logger.error(f"Faltan columnas requeridas en el archivo Excel: {columnas_faltantes}")
                return False
            
            # Limpiar valores NaN y espacios en blanco
            self.df_alm = self.df_alm.fillna('')
            for col in self.df_alm.columns:
                if self.df_alm[col].dtype == 'object':
                    self.df_alm[col] = self.df_alm[col].astype(str).str.strip()
            
            self.total_registros = len(self.df_alm)
            logger.info(f"Datos cargados exitosamente. Total de registros: {self.total_registros}")
            return True
            
        except Exception as e:
            logger.error(f"Error al cargar datos desde Excel: {e}")
            return False
    
    def _formatear_fecha(self, fecha_str: Any) -> Optional[str]:
        # Manejar valores nulos o NaT de pandas
        if pd.isna(fecha_str) or fecha_str == '':
            return None
        # Si es objeto datetime o Timestamp
        if isinstance(fecha_str, (datetime.date, datetime.datetime)):
            try:
                return fecha_str.strftime('%Y-%m-%d')
            except Exception:
                return None
        # Intentar formatos con posible componente horario
        formatos = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
        for fmt in formatos:
            try:
                fecha = datetime.datetime.strptime(str(fecha_str), fmt)
                return fecha.strftime('%Y-%m-%d')
            except ValueError:
                continue
        logger.warning(f"No se pudo formatear la fecha: {fecha_str}")
        return None
    
    def _formatear_telefono(self, telefono: str) -> Tuple[str, str]:
        """
        Formatea un número de teléfono separando el código de área y el número.
        
        Args:
            telefono: Número de teléfono en formato (código)número
            
        Returns:
            Tuple[str, str]: (código_area, número)
        """
        if not telefono or telefono == '':
            return '', ''
        
        # Buscar patrón (código)número
        match = re.search(r'\(([^)]+)\)\s*(\d+)', telefono)
        if match:
            codigo_area = match.group(1).strip()
            numero = match.group(2).strip()
            return codigo_area, numero
        
        # Si no tiene formato de paréntesis, devolver el número completo
        return '', telefono.strip()
    
    def _formatear_sexo(self, sexo: Any) -> Optional[str]:
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
    
    def migrar_informacion_personal(self) -> bool:
        """
        Migra la información personal de los estudiantes a la tabla informacion_personal.
        
        Returns:
            bool: True si la migración fue exitosa, False en caso contrario
        """
        try:
            logger.info("Iniciando migración de información personal...")
            
            for index, row in self.df_alm.iterrows():
                doc_id = str(row['A_ID']).strip()
                
                # Validar documento de identidad
                if not doc_id or doc_id == '':
                    logger.warning(f"Registro {index+1}: Documento de identidad vacío, se omitirá")
                    continue
                
                # Formatear datos
                nombres = str(row['A_NOMBRE']).strip()
                apellidos = str(row['A_APELLIDO']).strip()
                fecha_nacimiento = self._formatear_fecha(row.get('A_FNACIMIE', ''))
                sexo = self._formatear_sexo(row.get('A_SEXO', ''))
                estado_civil = self._formatear_estado_civil(row.get('A_ECIVIL', ''))
                nacionalidad = str(row.get('A_NACIONAL', '')).strip()
                lugar_nacimiento = str(row.get('A_LNACIMIE', '')).strip()
                correo = ''
                
                # Buscar correo en la dirección (muchas veces se usa este campo para el correo)
                direccion = str(row.get('A_DIRECCIO', '')).strip()
                if '@' in direccion:
                    correo = direccion
                
                fecha_registro = self._formatear_fecha(row.get('A_FINGRESO', ''))
                
                # Verificar si el estudiante ya existe
                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ? AND tipo_documento = 'cedula'",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()
                
                if resultado:
                    logger.warning(f"Estudiante con documento {doc_id} ya existe, se actualizará")
                    
                    # Actualizar información existente
                    self.cursor.execute("""
                        UPDATE informacion_personal 
                        SET nombres = ?, apellidos = ?, fecha_nacimiento = ?, sexo = ?, 
                            estado_civil = ?, nacionalidad = ?, lugar_nacimiento = ?, 
                            correo_electronico = ?, fecha_registro = ?
                        WHERE documento_identidad = ? AND tipo_documento = 'cedula'
                    """, (
                        nombres, apellidos, fecha_nacimiento, sexo, 
                        estado_civil, nacionalidad, lugar_nacimiento, 
                        correo, fecha_registro, doc_id
                    ))
                    
                else:
                    # Insertar nuevo registro
                    self.cursor.execute("""
                        INSERT INTO informacion_personal (
                            documento_identidad, tipo_documento, nombres, apellidos, 
                            fecha_nacimiento, sexo, estado_civil, nacionalidad, 
                            lugar_nacimiento, correo_electronico, fecha_registro, tipo
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        doc_id, 'cedula', nombres, apellidos, 
                        fecha_nacimiento, sexo, estado_civil, nacionalidad, 
                        lugar_nacimiento, correo, fecha_registro, 'estudiante'
                    ))
                
                self.conteo_migraciones["personal"] += 1
                
                if index % 50 == 0:  # Hacer commit cada 50 registros
                    self.conn.commit()
                    logger.info(f"Procesados {index+1} registros de {self.total_registros}...")
            
            self.conn.commit()
            logger.info(f"Migración de información personal completada. Registros procesados: {self.conteo_migraciones['personal']}")
            return True
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar información personal: {e}")
            return False
    
    def migrar_telefonos(self) -> bool:
        """
        Migra la información de teléfonos de los estudiantes a la tabla telefonos.
        
        Returns:
            bool: True si la migración fue exitosa, False en caso contrario
        """
        try:
            logger.info("Iniciando migración de teléfonos...")
            
            for index, row in self.df_alm.iterrows():
                doc_id = str(row['A_ID']).strip()
                
                # Validar documento de identidad
                if not doc_id or doc_id == '':
                    continue
                
                # Obtener el id de la persona
                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ? AND tipo_documento = 'cedula'",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()
                
                if not resultado:
                    logger.warning(f"No se encontró registro de persona para el documento {doc_id}, no se migrarán teléfonos")
                    continue
                
                persona_id = resultado[0]
                telefonos_migrados = 0
                
                # Procesar teléfonos
                for i, tel_campo in enumerate(['A_TEL1', 'A_TEL2', 'A_TEL3']):
                    telefono = str(row.get(tel_campo, '')).strip()
                    if telefono and telefono != '()' and telefono != '( )':
                        codigo_area, numero = self._formatear_telefono(telefono)
                        
                        if numero:
                            # Determinar si es telefono principal (el primero no vacío)
                            es_principal = 1 if telefonos_migrados == 0 else 0
                            
                            # Verificar si el teléfono ya existe para esta persona
                            self.cursor.execute(
                                "SELECT id FROM telefonos WHERE persona_id = ? AND numero = ?",
                                (persona_id, numero)
                            )
                            tel_existente = self.cursor.fetchone()
                            
                            if tel_existente:
                                # Actualizar teléfono existente
                                self.cursor.execute("""
                                    UPDATE telefonos 
                                    SET tipo_telefono = ?, principal = ?
                                    WHERE persona_id = ? AND numero = ?
                                """, (
                                    'movil', es_principal, persona_id, numero
                                ))
                            else:
                                # Insertar nuevo teléfono
                                self.cursor.execute("""
                                    INSERT INTO telefonos (persona_id, tipo_telefono, numero, principal)
                                    VALUES (?, ?, ?, ?)
                                """, (
                                    persona_id, 'movil', numero, es_principal
                                ))
                            
                            telefonos_migrados += 1
                
                self.conteo_migraciones["telefonos"] += telefonos_migrados
                
                if index % 50 == 0:  # Hacer commit cada 50 registros
                    self.conn.commit()
            
            self.conn.commit()
            logger.info(f"Migración de teléfonos completada. Registros procesados: {self.conteo_migraciones['telefonos']}")
            return True
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar teléfonos: {e}")
            return False
    
    def migrar_direcciones(self) -> bool:
        """
        Migra la información de direcciones de los estudiantes a la tabla direcciones.
        
        Returns:
            bool: True si la migración fue exitosa, False en caso contrario
        """
        try:
            logger.info("Iniciando migración de direcciones...")
            
            for index, row in self.df_alm.iterrows():
                doc_id = str(row['A_ID']).strip()
                
                # Validar documento de identidad
                if not doc_id or doc_id == '':
                    continue
                
                # Obtener el id de la persona
                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ? AND tipo_documento = 'cedula'",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()
                
                if not resultado:
                    continue
                
                persona_id = resultado[0]
                
                # Procesar dirección
                estado = str(row.get('A_EDORESID', '')).strip()
                municipio = str(row.get('A_MUNRESID', '')).strip()
                direccion_completa = str(row.get('A_DIRECCIO', '')).strip()
                
                # Si la dirección completa contiene un correo electrónico, no la consideramos dirección
                if direccion_completa and '@' not in direccion_completa:
                    # Verificar si ya existe una dirección para esta persona
                    self.cursor.execute(
                        "SELECT id FROM direcciones WHERE persona_id = ?",
                        (persona_id,)
                    )
                    dir_existente = self.cursor.fetchone()
                    
                    if dir_existente:
                        # Actualizar dirección existente
                        self.cursor.execute("""
                            UPDATE direcciones 
                            SET estado = ?, municipio = ?, direccion_completa = ?
                            WHERE persona_id = ?
                        """, (
                            estado, municipio, direccion_completa, persona_id
                        ))
                    else:
                        # Insertar nueva dirección
                        self.cursor.execute("""
                            INSERT INTO direcciones (
                                persona_id, estado, municipio, parroquia, 
                                sector, calle, casa_edificio, piso_apartamento, 
                                direccion_completa, tipo_direccion, principal
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            persona_id, estado, municipio, '', 
                            '', '', '', '',
                            direccion_completa, 'residencia', 1
                        ))
                    
                    self.conteo_migraciones["direcciones"] += 1
                
                if index % 50 == 0:  # Hacer commit cada 50 registros
                    self.conn.commit()
            
            self.conn.commit()
            logger.info(f"Migración de direcciones completada. Registros procesados: {self.conteo_migraciones['direcciones']}")
            return True
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar direcciones: {e}")
            return False
    
    def migrar_estudiantes(self) -> bool:
        """
        Migra la información académica de los estudiantes a la tabla estudiantes.
        
        Returns:
            bool: True si la migración fue exitosa, False en caso contrario
        """
        try:
            logger.info("Iniciando migración de información académica de estudiantes...")
            
            for index, row in self.df_alm.iterrows():
                doc_id = str(row['A_ID']).strip()
                
                # Validar documento de identidad
                if not doc_id or doc_id == '':
                    continue
                
                # Obtener el id de la persona
                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ? AND tipo_documento = 'cedula'",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()
                
                if not resultado:
                    continue
                
                persona_id = resultado[0]
                
                # Generar código único para el estudiante (basado en el documento de identidad)
                codigo_unico = f"EST{doc_id}"
                
                # Formatear datos académicos
                institucion_procedencia = str(row.get('A_NOMINSTI', '')).strip() if row.get('A_NOMINSTI') else ''
                if not institucion_procedencia and row.get('A_INSPROCE') == 'VERDADERO':
                    # Si hay un flag de institución pero no nombre específico
                    institucion_procedencia = "Institución Externa"
                
                mencion_bachiller = str(row.get('A_MENCIBAC', '')).strip()
                fecha_grado_bachiller = self._formatear_fecha(row.get('A_FGRABACH', ''))
                fecha_ingreso = self._formatear_fecha(row.get('A_FINGRESO', ''))
                
                condicion = None
                if row.get('A_CONDICIO'):
                    condicion_valor = str(row.get('A_CONDICIO')).strip()
                    if condicion_valor.lower() in ['verdadero', 'true', '1']:
                        condicion = 'Regular'
                
                oyente = 1 if row.get('A_OYENTE') and str(row.get('A_OYENTE')).lower() in ['verdadero', 'true', '1'] else 0
                
                situacion_academica = 'Activo'
                if row.get('A_SITUACIO'):
                    sit_valor = str(row.get('A_SITUACIO')).strip().lower()
                    if 'retir' in sit_valor:
                        situacion_academica = 'Retirado'
                    elif 'gradu' in sit_valor or 'egresa' in sit_valor:
                        situacion_academica = 'Graduado'
                    elif 'inactiv' in sit_valor:
                        situacion_academica = 'Inactivo'
                
                # Verificar si el estudiante ya existe
                self.cursor.execute(
                    "SELECT id FROM estudiantes WHERE persona_id = ?",
                    (persona_id,)
                )
                estudiante_existente = self.cursor.fetchone()
                
                if estudiante_existente:
                    # Actualizar estudiante existente
                    self.cursor.execute("""
                        UPDATE estudiantes 
                        SET institucion_procedencia = ?, mencion_bachiller = ?, 
                            fecha_grado_bachiller = ?, fecha_ingreso = ?, 
                            condicion = ?, oyente = ?, situacion_academica = ?
                        WHERE persona_id = ?
                    """, (
                        institucion_procedencia, mencion_bachiller, 
                        fecha_grado_bachiller, fecha_ingreso, 
                        condicion, oyente, situacion_academica, persona_id
                    ))
                else:
                    # Insertar nuevo estudiante
                    self.cursor.execute("""
                        INSERT INTO estudiantes (
                            persona_id, codigo_unico, institucion_procedencia, mencion_bachiller, 
                            fecha_grado_bachiller, profesion, fecha_grado_profesional, 
                            fecha_ingreso, condicion, oyente, situacion_academica
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        persona_id, codigo_unico, institucion_procedencia, mencion_bachiller, 
                        fecha_grado_bachiller, None, None, 
                        fecha_ingreso, condicion, oyente, situacion_academica
                    ))
                
                self.conteo_migraciones["estudiantes"] += 1
                
                if index % 50 == 0:  # Hacer commit cada 50 registros
                    self.conn.commit()
            
            self.conn.commit()
            logger.info(f"Migración de información académica de estudiantes completada. Registros procesados: {self.conteo_migraciones['estudiantes']}")
            return True
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar información académica de estudiantes: {e}")
            return False
    
    def ejecutar_migracion(self) -> Tuple[bool, Dict[str, int]]:
        """
        Ejecuta el proceso completo de migración.
        
        Returns:
            Tuple[bool, Dict[str, int]]: (éxito, conteo de registros migrados por tabla)
        """
        exito = True
        
        # Conectar a la base de datos
        if not self.conectar_db():
            return False, self.conteo_migraciones
        
        try:
            # Seleccionar y cargar archivo Excel
            archivo_excel = self.seleccionar_archivo_excel()
            if not archivo_excel:
                logger.warning("No se seleccionó ningún archivo. Operación cancelada.")
                return False, self.conteo_migraciones
            
            if not self.cargar_datos_excel(archivo_excel):
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
            elif not self.migrar_estudiantes():
                self.conn.rollback()
                exito = False
            else:
                # Si todo salió bien, confirmar los cambios
                self.conn.commit()
                logger.info("Migración completada exitosamente")
        
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error durante la migración: {e}")
            exito = False
        
        finally:
            # Cerrar conexión a la base de datos
            self.cerrar_db()
        
        return exito, self.conteo_migraciones


def main():
    """Función principal del script de migración."""
    print("=" * 60)
    print("SISTEMA DE MIGRACIÓN DE DATOS ALM A NUEVA ESTRUCTURA SQLITE3")
    print("=" * 60)
    print("\nEste script migra los datos de la tabla ALM desde un archivo Excel")
    print("a la nueva estructura de base de datos SQLite3.")
    print("\nSeleccione la base de datos SQLite3 de destino...")
    
    # Seleccionar la base de datos SQLite3
    root = Tk()
    root.withdraw()
    db_path = filedialog.askopenfilename(
        title="Seleccione la base de datos SQLite3 de destino",
        filetypes=[("Bases de datos SQLite3", "*.db;*.sqlite;*.sqlite3")]
    )
    root.destroy()
    
    if not db_path:
        print("No se seleccionó ninguna base de datos. Operación cancelada.")
        return
    
    # Crear y ejecutar el migrador
    migrador = MigradorALM(db_path)
    exito, conteo = migrador.ejecutar_migracion()
    
    # Mostrar resumen de la migración
    print("\n" + "=" * 60)
    print("RESUMEN DE LA MIGRACIÓN")
    print("=" * 60)
    print(f"Base de datos: {db_path}")
    print(f"Estado de la migración: {'EXITOSA' if exito else 'FALLIDA'}")
    print("\nRegistros migrados:")
    print(f"- Información personal: {conteo['personal']}")
    print(f"- Teléfonos: {conteo['telefonos']}")
    print(f"- Direcciones: {conteo['direcciones']}")
    print(f"- Estudiantes: {conteo['estudiantes']}")
    print("\nConsulte el archivo de log para más detalles.")


if __name__ == "__main__":
    main()
