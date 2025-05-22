# archivo migrador_alm.py
from migrador_base import MigradorBase
import logging
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger("migracion")

class MigradorALM(MigradorBase):
    """
    Clase para manejar la migración de datos de la tabla ALM a la nueva estructura SQLite3.
    """

    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.columnas_requeridas = [
            'A_ID', 'A_NOMBRE', 'A_APELLIDO', 'A_FINGRESO', 'A_FNACIMIE',
            'A_SEXO', 'A_ECIVIL', 'A_NACIONAL', 'A_LNACIMIE', 'A_TEL1',
            'A_TEL2', 'A_TEL3', 'A_EDORESID', 'A_MUNRESID', 'A_DIRECCIO'
        ]
        self.conteo_migraciones = {
            "informacion_personal": 0,
            "telefonos": 0,
            "direcciones": 0,
            "estudiantes": 0
            }
    
    def migrar_informacion_personal(self) -> bool:
        """Migra la información personal de estudiantes."""
        try:
            logger.info("Iniciando migración de información personal de estudiantes...")
            
            # Inicializar contadores para debugging
            contador_vacias = 0
            contador_un_digito = 0
            contador_actualizados = 0
            
            for index, row in self.df_data.iterrows():
                doc_id = self._validar_cedula(row.get('A_ID', ''))
                
                # Verificar cédula vacía
                if not doc_id:
                    contador_vacias += 1
                    logger.warning(f"Registro {index+1}: Documento de identidad vacío, se omitirá")
                    # Agregar información adicional para debugging
                    registro_info = row.to_dict()
                    registro_info['_numero_fila'] = index + 1
                    registro_info['_razon'] = 'cedula_vacia'
                    self.registros_cedula_vacia[index+1] = registro_info
                    continue
                
                # Verificar cédula de un solo dígito
                if doc_id == "CEDULA_UN_DIGITO":
                    contador_un_digito += 1
                    cedula_original = str(row.get('A_ID', '')).strip()
                    logger.warning(f"Registro {index+1}: Documento '{cedula_original}' tiene un solo dígito, se omitirá")
                    # Agregar información adicional para debugging
                    registro_info = row.to_dict()
                    registro_info['_numero_fila'] = index + 1
                    registro_info['_cedula_original'] = cedula_original
                    registro_info['_razon'] = 'cedula_un_digito'
                    self.registros_cedula_invalida[index+1] = registro_info
                    continue

                # ... resto del código existente hasta la parte de UPDATE ...
                

                nombres = str(row.get('A_NOMBRE', '')).strip()
                apellidos = str(row.get('A_APELLIDO', '')).strip()
                fecha_nacimiento = self._formatear_fecha(row.get('A_FNACIMIE', ''))
                sexo = self._formatear_sexo(row.get('A_SEXO', ''))
                estado_civil = self._formatear_estado_civil(row.get('A_ECIVIL', ''))
                nacionalidad = self._formatear_nacionalidad(row.get('A_NACIONAL', ''))
                lugar_nacimiento = str(row.get('A_LNACIMIE', '')).strip()
                correo = ''
                fecha_registro = self._formatear_fecha(row.get('A_FINGRESO', ''))
                pasaporte = str(row.get('A_PASSPORT', '')).strip() if 'A_PASSPORT' in row else ''

                direccion = str(row.get('A_DIRECCIO', '')).strip()
                if '@' in direccion:
                    correo = direccion

                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()


                if resultado:
                    contador_actualizados += 1
                    logger.warning(f"Estudiante con documento {doc_id} ya existe, se actualizará")
                    # Guardar registro que se está actualizando con información adicional
                    registro_info = row.to_dict()
                    registro_info['_numero_fila'] = index + 1
                    registro_info['_documento_id'] = doc_id
                    registro_info['_razon'] = 'actualizacion'
                    self.registros_actualizados[doc_id] = registro_info
                    
                    self.cursor.execute("""
                        UPDATE informacion_personal
                        SET nombres = ?, apellidos = ?, fecha_nacimiento = ?, sexo = ?,
                            estado_civil = ?, nacionalidad = ?, lugar_nacimiento = ?,
                            correo_electronico = ?, fecha_registro = ?, tipo = ?, pasaporte = ?
                        WHERE documento_identidad = ?
                    """, (
                        nombres, apellidos, fecha_nacimiento, sexo,
                        estado_civil, nacionalidad, lugar_nacimiento,
                        correo, fecha_registro, 'estudiante', pasaporte, doc_id
                    ))
                else:
                    self.cursor.execute("""
                        INSERT INTO informacion_personal (
                            documento_identidad, tipo_documento, nombres, apellidos,
                            fecha_nacimiento, sexo, estado_civil, nacionalidad,
                            lugar_nacimiento, correo_electronico, fecha_registro, tipo, pasaporte
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        doc_id, 'cedula', nombres, apellidos,
                        fecha_nacimiento, sexo, estado_civil, nacionalidad,
                        lugar_nacimiento, correo, fecha_registro, 'estudiante', pasaporte
                    ))

                self.conteo_migraciones['informacion_personal'] += 1

                if index % 50 == 0:
                    self.conn.commit()
                    logger.info(f"Procesados {index+1} registros de {self.total_registros}...")

            self.conn.commit()
            
            logger.info(f"Contadores finales - Vacías: {contador_vacias}, Un dígito: {contador_un_digito}, Actualizados: {contador_actualizados}")
            
            # Guardar registros problemáticos y actualizaciones
            self._guardar_registros_especiales()
            
            return True

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar información personal: {e}")
            return False

    def migrar_telefonos(self) -> bool:
        """Migra los teléfonos de estudiantes."""
        conteo = 0
        try:
            logger.info("Iniciando migración de teléfonos de estudiantes...")
            for index, row in self.df_data.iterrows():
                doc_id = self._validar_cedula(row.get('A_ID', ''))
                if not doc_id:
                    continue

                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()
                if not resultado:
                    logger.warning(f"No se encontró la persona con documento {doc_id} para migrar teléfonos")
                    continue

                persona_id = resultado[0]
                telefonos = [
                    ('movil', row.get('A_TEL1', '')),
                    ('casa', row.get('A_TEL2', '')),
                    ('otro', row.get('A_TEL3', ''))
                ]
                for i, (tipo, telefono) in enumerate(telefonos):
                    if not telefono or str(telefono).strip() == '' or str(telefono).strip().lower() in ['nan', 'none', 'null']:
                        continue
                    codigo_area, numero = self._formatear_telefono(str(telefono))
                    # Cambiar la validación: solo continuar si AMBOS están vacíos
                    if not numero or numero.strip() == '':
                        continue
                    principal = 1 if i == 0 else 0
                    self.cursor.execute(
                        "SELECT id FROM telefonos WHERE persona_id = ? AND numero = ?",
                        (persona_id, numero)
                    )
                    tel_existe = self.cursor.fetchone()
                    if tel_existe:
                        self.cursor.execute("""
                            UPDATE telefonos
                            SET tipo_telefono = ?, principal = ?
                            WHERE id = ?
                        """, (tipo, principal, tel_existe[0]))
                    else:
                        self.cursor.execute("""
                            INSERT INTO telefonos
                            (persona_id, tipo_telefono, numero, principal)
                            VALUES (?, ?, ?, ?)
                        """, (persona_id, tipo, (codigo_area+numero), principal))
                        conteo += 1

            self.conn.commit()
            self.conteo_migraciones['telefonos'] = conteo
            logger.info(f"Migración de teléfonos completada. Registros procesados: {conteo}")
            return True

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar teléfonos: {e}")
            return False

    def migrar_direcciones(self) -> bool:
        """Migra las direcciones de estudiantes."""
        conteo = 0
        try:
            logger.info("Iniciando migración de direcciones de estudiantes...")
            for index, row in self.df_data.iterrows():
                doc_id = self._validar_cedula(row.get('A_ID', ''))
                if not doc_id:
                    continue

                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()
                if not resultado:
                    logger.warning(f"No se encontró la persona con documento {doc_id} para migrar direcciones")
                    continue

                persona_id = resultado[0]
                estado = str(row.get('A_EDORESID', '')).strip()
                municipio = str(row.get('A_MUNRESID', '')).strip()
                direccion_completa = str(row.get('A_DIRECCIO', '')).strip()
                if not direccion_completa or not estado or not municipio:
                    continue
                if '@' in direccion_completa:
                    continue

                self.cursor.execute(
                    "SELECT id FROM direcciones WHERE persona_id = ? AND direccion_completa = ?",
                    (persona_id, direccion_completa)
                )
                dir_existe = self.cursor.fetchone()
                if dir_existe:
                    self.cursor.execute("""
                        UPDATE direcciones
                        SET estado = ?, municipio = ?
                        WHERE id = ?
                    """, (estado, municipio, dir_existe[0]))
                else:
                    self.cursor.execute("""
                        INSERT INTO direcciones
                        (persona_id, estado, municipio, direccion_completa, tipo_direccion, principal)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (persona_id, estado, municipio, direccion_completa, 'residencia', 1))
                    conteo += 1

            self.conn.commit()
            self.conteo_migraciones['direcciones'] = conteo
            logger.info(f"Migración de direcciones completada. Registros procesados: {conteo}")
            return True

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar direcciones: {e}")
            return False

    def migrar_especifico(self) -> bool:
        """Migra la información específica de estudiantes."""
        return self.migrar_estudiantes()

    def migrar_estudiantes(self) -> bool:
        """Migra los datos específicos de estudiantes."""
        conteo = 0
        try:
            logger.info("Iniciando migración de información específica de estudiantes...")
            
            # Diccionario para rastrear códigos únicos y evitar duplicados
            codigos_unicos_usados = set()
            
            for index, row in self.df_data.iterrows():
                doc_id = self._validar_cedula(row.get('A_ID', ''))
                if not doc_id or doc_id == "CEDULA_UN_DIGITO":
                    continue

                self.cursor.execute(
                    "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                    (doc_id,)
                )
                resultado = self.cursor.fetchone()
                if not resultado:
                    logger.warning(f"No se encontró la persona con documento {doc_id} para migrar datos específicos")
                    continue

                persona_id = resultado[0]
                
                # Generar código único
                codigo_unico_raw = str(row.get('RUSNIE', '')).strip() if 'RUSNIE' in row else ''
                
                # Si RUSNIE está vacío o no existe, generar código único basado en documento
                if not codigo_unico_raw:
                    codigo_unico = None
                else:
                    codigo_unico = codigo_unico_raw
                
                # Verificar si el código único ya está siendo usado en esta migración
                contador_duplicado = 1
                codigo_unico_original = codigo_unico
                while codigo_unico in codigos_unicos_usados:
                    codigo_unico = f"{codigo_unico_original}-{contador_duplicado}"
                    contador_duplicado += 1
                
                # Verificar si el código único ya existe en la base de datos
                self.cursor.execute(
                    "SELECT id, persona_id FROM estudiantes WHERE codigo_unico = ?",
                    (codigo_unico,)
                )
                codigo_existe = self.cursor.fetchone()
                
                # Si existe y no es del mismo estudiante, generar un código alternativo
                if codigo_existe and codigo_existe[1] != persona_id:
                    contador_bd = 1
                    codigo_unico_temp = f"{codigo_unico_original}-BD{contador_bd}"
                    while True:
                        self.cursor.execute(
                            "SELECT id FROM estudiantes WHERE codigo_unico = ?",
                            (codigo_unico_temp,)
                        )
                        if not self.cursor.fetchone():
                            codigo_unico = codigo_unico_temp
                            break
                        contador_bd += 1
                        codigo_unico_temp = f"{codigo_unico_original}-BD{contador_bd}"
                
                # Agregar a la lista de códigos usados
                codigos_unicos_usados.add(codigo_unico)
                
                # Procesar otros campos
                institucion_procedencia = str(row.get('A_NOMINSTI', '')).strip() if 'A_NOMINSTI' in row else ''
                mencion_bachiller = str(row.get('A_MENCIBAC', '')).strip() if 'A_MENCIBAC' in row else ''
                fecha_grado_bachiller = self._formatear_fecha(row.get('A_FGRABACH', '')) if 'A_FGRABACH' in row else None
                profesion = str(row.get('A_PROFESIO', '')).strip() if 'A_PROFESIO' in row else ''
                fecha_grado_profesional = self._formatear_fecha(row.get('A_FGRAPROF', '')) if 'A_FGRAPROF' in row else None
                fecha_ingreso = self._formatear_fecha(row.get('A_FINGRESO', ''))
                condicion = str(row.get('A_CONDICIO', '')).strip()
                
                # Normalizar condición
                if condicion.lower() in ['regular', 'reg']:
                    condicion = 'Regular'
                elif condicion.lower() in ['repitente', 'rep']:
                    condicion = 'Repitente'
                elif condicion.lower() in ['reingreso', 'rei']:
                    condicion = 'Reingreso'
                elif condicion.lower() in ['transferencia', 'trans']:
                    condicion = 'Transferencia'
                else:
                    condicion = 'Regular'
                
                oyente = str(row.get('A_OYENTE', '')).strip().lower()
                es_oyente = 1 if oyente in ['verdadero', 'true', '1', 'si', 'sí', 'yes'] else 0

                # Verificar si ya existe un estudiante para esta persona
                self.cursor.execute(
                    "SELECT id FROM estudiantes WHERE persona_id = ?",
                    (persona_id,)
                )
                est_existe = self.cursor.fetchone()
                
                if est_existe:
                    # Actualizar registro existente
                    self.cursor.execute("""
                        UPDATE estudiantes
                        SET codigo_unico = ?, institucion_procedencia = ?, mencion_bachiller = ?, fecha_grado_bachiller = ?,
                            profesion = ?, fecha_grado_profesional = ?, fecha_ingreso = ?,
                            condicion = ?, oyente = ?
                        WHERE id = ?
                    """, (
                        codigo_unico, institucion_procedencia, mencion_bachiller, fecha_grado_bachiller,
                        profesion, fecha_grado_profesional, fecha_ingreso,
                        condicion, es_oyente, est_existe[0]
                    ))
                    logger.info(f"Estudiante actualizado - Persona ID: {persona_id}, Código: {codigo_unico}")
                else:
                    # Insertar nuevo registro
                    self.cursor.execute("""
                        INSERT INTO estudiantes
                        (persona_id, codigo_unico, institucion_procedencia, mencion_bachiller,
                        fecha_grado_bachiller, profesion, fecha_grado_profesional,
                        fecha_ingreso, condicion, oyente)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        persona_id, codigo_unico, institucion_procedencia, mencion_bachiller,
                        fecha_grado_bachiller, profesion, fecha_grado_profesional,
                        fecha_ingreso, condicion, es_oyente
                    ))
                    conteo += 1
                    logger.info(f"Estudiante insertado - Persona ID: {persona_id}, Código: {codigo_unico}")

                # Commit cada 50 registros para evitar problemas de memoria
                if index % 50 == 0:
                    self.conn.commit()
                    logger.info(f"Procesados {index+1} estudiantes de {self.total_registros}...")

            self.conn.commit()
            self.conteo_migraciones['estudiantes'] = conteo
            logger.info(f"Migración de datos específicos de estudiantes completada. Registros procesados: {conteo}")
            logger.info(f"Total de códigos únicos generados: {len(codigos_unicos_usados)}")
            return True

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error al migrar datos específicos de estudiantes: {e}")
            return False
    
    def ejecutar_migracion(self) -> Tuple[bool, Dict[str, int]]:
        """
        Ejecuta el proceso completo de migración.
        Returns:
            Tuple[bool, Dict[str, int]]: (éxito, conteo de registros migrados por tabla)
        """
        return super().ejecutar_migracion(self.columnas_requeridas)
        
    def _guardar_registros_especiales(self):
        """Guarda los registros especiales en archivos JSON separados"""
        import json
        import os
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Función auxiliar para guardar con manejo de errores
        def guardar_archivo_json(datos, nombre_archivo, descripcion):
            try:
                # Verificar que los datos no estén vacíos
                if not datos:
                    logger.info(f"No hay {descripcion} para guardar")
                    return

                ruta_completa = os.path.join('reportes', nombre_archivo)

                
                # Convertir datos a formato serializable
                datos_serializables = {}
                for key, value in datos.items():
                    if isinstance(value, dict):
                        # Limpiar valores que no se pueden serializar
                        datos_limpios = {}
                        for k, v in value.items():
                            try:
                                # Convertir pandas/numpy types a tipos básicos de Python
                                if hasattr(v, 'item'):  # numpy types
                                    datos_limpios[k] = v.item()
                                elif hasattr(v, 'to_pydatetime'):  # pandas datetime
                                    datos_limpios[k] = str(v)
                                elif str(type(v)).startswith('<class \'pandas'):  # otros tipos pandas
                                    datos_limpios[k] = str(v)
                                else:
                                    datos_limpios[k] = v
                            except Exception as e:
                                logger.warning(f"Error al procesar campo {k}: {e}")
                                datos_limpios[k] = str(v)
                        datos_serializables[str(key)] = datos_limpios
                    else:
                        datos_serializables[str(key)] = str(value)
                
                # Escribir archivo con flush explícito
                with open(ruta_completa, "w", encoding="utf-8") as f:
                    json.dump(datos_serializables, f, ensure_ascii=False, indent=2, default=str)
                    f.flush()  # Asegurar que se escriba al disco
                
                # Verificar que el archivo se escribió correctamente
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    verificacion = json.load(f)
                    if len(verificacion) != len(datos_serializables):
                        raise Exception("El archivo no se guardó completamente")
                
                logger.info(f"{descripcion} guardados en: {ruta_completa} ({len(datos_serializables)} registros)")
                
            except Exception as e:
                logger.error(f"Error al guardar {descripcion}: {e}")
                # Intentar guardar como archivo de texto plano como respaldo
                try:
                    nombre_txt = nombre_archivo.replace('.json', '_respaldo.txt')
                    with open(nombre_txt, "w", encoding="utf-8") as f:
                        f.write(f"{descripcion}:\n")
                        f.write("="*50 + "\n")
                        for key, value in datos.items():
                            f.write(f"\nRegistro {key}:\n")
                            if isinstance(value, dict):
                                for k, v in value.items():
                                    f.write(f"  {k}: {v}\n")
                            else:
                                f.write(f"  {value}\n")
                            f.write("-"*30 + "\n")
                        f.flush()
                    logger.info(f"Archivo de respaldo creado: {nombre_txt}")
                except Exception as e2:
                    logger.error(f"Error al crear archivo de respaldo: {e2}")
        
        # Guardar cada tipo de registro
        if self.registros_cedula_vacia:
            archivo_vacias = f"ALM_registros_cedula_vacia_{timestamp}.json"
            guardar_archivo_json(self.registros_cedula_vacia, archivo_vacias, "Registros con cédula vacía")
        
        if self.registros_cedula_invalida:
            archivo_invalidas = f"ALM_registros_cedula_un_digito_{timestamp}.json"
            guardar_archivo_json(self.registros_cedula_invalida, archivo_invalidas, "Registros con cédula de un dígito")
        
        if self.registros_actualizados:
            archivo_actualizados = f"ALM_registros_actualizados_{timestamp}.json"
            guardar_archivo_json(self.registros_actualizados, archivo_actualizados, "Registros actualizados")

        # Mostrar resumen
        total_problematicos = len(self.registros_cedula_vacia) + len(self.registros_cedula_invalida)
        total_actualizados = len(self.registros_actualizados)
        
        logger.info(f"\nRESUMEN DE REGISTROS ESPECIALES:")
        logger.info(f"- Cédulas vacías: {len(self.registros_cedula_vacia)}")
        logger.info(f"- Cédulas de un dígito: {len(self.registros_cedula_invalida)}")
        logger.info(f"- Registros actualizados: {len(self.registros_actualizados)}")
        logger.info(f"- Total registros problemáticos: {total_problematicos}")
        
        
        
