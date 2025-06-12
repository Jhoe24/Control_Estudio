# archivo migrador_dct.py
# archivo migrador_dct.py
from migrador_base import MigradorBase
import logging
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger("migracion")

class MigradorDCT(MigradorBase):
    """
    Clase para manejar la migración de datos de la tabla DCT a la nueva estructura SQLite3.
    """

    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.columnas_requeridas = [
            'D_ID', 'D_NOMBRE', 'D_SEXO', 'D_FNACI', 'D_DIRECC',
            'D_TEL1', 'D_TEL2', 'D_CORREO', 'D_ABREVIA', 'D_AUXILIAR'
        ]
        self.conteo_migraciones = {
            "informacion_personal": 0,
            "telefonos": 0,
            "direcciones": 0,
            "docentes": 0
        }

    def _separar_nombre_apellido(self, nombre_completo: str) -> Tuple[str, str]:
        """
        Separa un nombre completo en nombres y apellidos.

        Args:
            nombre_completo: Nombre completo a separar

        Returns:
            Tuple[str, str]: (nombres, apellidos)
        """
        if not nombre_completo or nombre_completo.strip() == '':
            return '', ''

        partes = nombre_completo.strip().split()
        if len(partes) == 1:
            return partes[0], ''
        elif len(partes) == 2:
            return partes[0], partes[1]
        elif len(partes) == 3:
            return f"{partes[0]} {partes[1]}", partes[2]
        else:
            # Para nombres con más de 3 partes, asumir que las primeras dos son nombres
            # y el resto son apellidos
            nombres = ' '.join(partes[:2])
            apellidos = ' '.join(partes[2:])
            return nombres, apellidos

    # def _validar_correo(self, correo: str) -> bool:
    #     """
    #     Valida que un correo electrónico tenga un formato básico válido.
        
    #     Args:
    #         correo: Correo a validar
            
    #     Returns:
    #         bool: True si es válido, False en caso contrario
    #     """
    #     if not correo or not isinstance(correo, str):
    #         return False
        
    #     correo = correo.strip()
    #     if not correo:
    #         return False
            
    #     # Validación básica: debe contener @ y al menos un punto después del @
    #     if '@' not in correo:
    #         return False
            
    #     partes = correo.split('@')
    #     if len(partes) != 2:
    #         return False
            
    #     usuario, dominio = partes
    #     if not usuario or not dominio:
    #         return False
            
    #     if '.' not in dominio:
    #         return False
            
    #     return True

    def migrar_informacion_personal(self) -> bool:
        """Migra la información personal de docentes."""
        try:
            logger.info("Iniciando migración de información personal de docentes...")
            
            # Verificar que hay datos para procesar
            if self.df_data is None or self.df_data.empty:
                logger.error("No hay datos de docentes para procesar")
                return False
            
            logger.info(f"Total de registros de docentes a procesar: {len(self.df_data)}")
            
            # Inicializar contadores para debugging
            contador_vacias = 0
            contador_un_digito = 0
            contador_actualizados = 0
            contador_nuevos = 0
            contador_errores = 0
            
            for index, row in self.df_data.iterrows():
                try:
                    doc_id = self._validar_cedula(row.get('D_ID', ''))
                    
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
                        cedula_original = str(row.get('D_ID', '')).strip()
                        logger.warning(f"Registro {index+1}: Documento '{cedula_original}' tiene un solo dígito, se omitirá")
                        # Agregar información adicional para debugging
                        registro_info = row.to_dict()
                        registro_info['_numero_fila'] = index + 1
                        registro_info['_cedula_original'] = cedula_original
                        registro_info['_razon'] = 'cedula_un_digito'
                        self.registros_cedula_invalida[index+1] = registro_info
                        continue

                    # Formatear datos
                    nombre_completo = str(row.get('D_NOMBRE', '')).strip()
                    nombres, apellidos = self._separar_nombre_apellido(nombre_completo)
                    fecha_nacimiento = self._formatear_fecha(row.get('D_FNACI', ''))
                    sexo = self._formatear_sexo(row.get('D_SEXO', ''))
                    correo = str(row.get('D_CORREO', '')).strip()
                    
                    # Validar correo electrónico
                    if correo and not self._validar_correo(correo):
                        logger.warning(f"Correo inválido para documento {doc_id}: {correo}")
                        correo = ''  # Limpiar correo inválido

                    # Verificar si el docente ya existe
                    self.cursor.execute(
                        "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                        (doc_id,)
                    )
                    resultado = self.cursor.fetchone()

                    if resultado:
                        contador_actualizados += 1
                        logger.debug(f"Docente con documento {doc_id} ya existe, se actualizará")
                        # Guardar registro que se está actualizando con información adicional
                        registro_info = row.to_dict()
                        registro_info['_numero_fila'] = index + 1
                        registro_info['_documento_id'] = doc_id
                        registro_info['_razon'] = 'actualizacion'
                        self.registros_actualizados[doc_id] = registro_info

                        # Actualizar información existente
                        self.cursor.execute("""
                            UPDATE informacion_personal
                            SET nombres = ?, apellidos = ?, fecha_nacimiento = ?, sexo = ?,
                                correo_electronico = ?, tipo = ?
                            WHERE documento_identidad = ?
                        """, (
                            nombres, apellidos, fecha_nacimiento, sexo,
                            correo, 'docente', doc_id
                        ))
                    else:
                        contador_nuevos += 1
                        # Insertar nuevo registro
                        self.cursor.execute("""
                            INSERT INTO informacion_personal (
                                documento_identidad, tipo_documento, nombres, apellidos,
                                fecha_nacimiento, sexo, correo_electronico, fecha_registro, tipo
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            doc_id, 'cedula', nombres, apellidos,
                            fecha_nacimiento, sexo, correo, None, 'docente'
                        ))

                    self.conteo_migraciones['informacion_personal'] += 1

                    # Commit periódico para evitar problemas de memoria
                    if (index + 1) % 50 == 0:
                        self.conn.commit()
                        logger.info(f"Procesados {index+1} registros de {len(self.df_data)}...")

                except Exception as e:
                    contador_errores += 1
                    logger.error(f"Error procesando registro {index+1}: {e}")
                    # Continuar con el siguiente registro en lugar de fallar completamente
                    continue

            self.conn.commit()
            
            logger.info(f"Migración de información personal completada:")
            logger.info(f"- Registros nuevos: {contador_nuevos}")
            logger.info(f"- Registros actualizados: {contador_actualizados}")
            logger.info(f"- Cédulas vacías omitidas: {contador_vacias}")
            logger.info(f"- Cédulas inválidas omitidas: {contador_un_digito}")
            logger.info(f"- Errores procesando: {contador_errores}")
            logger.info(f"- Total procesados exitosamente: {self.conteo_migraciones['informacion_personal']}")
            
            # Guardar registros problemáticos y actualizaciones
            self._guardar_registros_especiales()
            
            # Verificar que realmente se insertaron datos
            self.cursor.execute("SELECT COUNT(*) FROM informacion_personal WHERE tipo = 'docente'")
            total_docentes = self.cursor.fetchone()[0]
            logger.info(f"Total de docentes en la base de datos: {total_docentes}")
            
            return True

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error crítico al migrar información personal: {e}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return False

    def migrar_telefonos(self) -> bool:
        """Migra los teléfonos de docentes."""
        conteo_nuevos = 0
        conteo_actualizados = 0
        
        try:
            logger.info("Iniciando migración de teléfonos de docentes...")
            
            # Verificar que hay datos para procesar
            if self.df_data is None or self.df_data.empty:
                logger.warning("No hay datos de docentes para procesar teléfonos")
                return True  # No es un error, simplemente no hay datos
            
            for index, row in self.df_data.iterrows():
                try:
                    doc_id = self._validar_cedula(row.get('D_ID', ''))
                    if not doc_id or doc_id == "CEDULA_UN_DIGITO":
                        continue

                    # Buscar la persona en la base de datos
                    self.cursor.execute(
                        "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                        (doc_id,)
                    )
                    resultado = self.cursor.fetchone()
                    if not resultado:
                        logger.warning(f"No se encontró la persona con documento {doc_id} para migrar teléfonos")
                        continue

                    persona_id = resultado[0]
                    
                    # Procesar teléfonos
                    telefonos = [
                        ('movil', row.get('D_TEL1', '')),
                        ('casa', row.get('D_TEL2', ''))
                    ]

                    for i, (tipo, telefono) in enumerate(telefonos):
                        # Validar que el teléfono no esté vacío
                        if not telefono or str(telefono).strip() == '' or str(telefono).strip().lower() in ['nan', 'none', 'null']:
                            continue
                        
                        telefono_str = str(telefono).strip()
                        # Verificar si es un teléfono válido (no solo paréntesis vacíos)
                        if telefono_str in ['()', '( )', '(  )', '']:
                            continue

                        codigo_area, numero = self._formatear_telefono(telefono_str)
                        # Solo continuar si hay un número válido
                        if not numero or numero.strip() == '':
                            logger.warning(f"Teléfono inválido para documento {doc_id}: {telefono_str}")
                            continue

                        principal = 1 if i == 0 else 0
                        numero_completo = codigo_area + numero
                        
                        # Verificar si el teléfono ya existe para esta persona
                        self.cursor.execute(
                            "SELECT id FROM telefonos WHERE persona_id = ? AND numero = ?",
                            (persona_id, numero_completo)
                        )
                        tel_existe = self.cursor.fetchone()
                        
                        if tel_existe:
                            # Actualizar teléfono existente
                            self.cursor.execute("""
                                UPDATE telefonos
                                SET tipo_telefono = ?, principal = ?
                                WHERE id = ?
                            """, (tipo, principal, tel_existe[0]))
                            conteo_actualizados += 1
                        else:
                            # Insertar nuevo teléfono
                            self.cursor.execute("""
                                INSERT INTO telefonos
                                (persona_id, tipo_telefono, numero, principal)
                                VALUES (?, ?, ?, ?)
                            """, (persona_id, tipo, numero_completo, principal))
                            conteo_nuevos += 1

                    # Commit periódico
                    if (index + 1) % 50 == 0:
                        self.conn.commit()
                        logger.info(f"Procesados teléfonos para {index+1} docentes de {len(self.df_data)}...")

                except Exception as e:
                    logger.error(f"Error procesando teléfonos del registro {index+1}: {e}")
                    continue

            self.conn.commit()
            self.conteo_migraciones['telefonos'] = conteo_nuevos + conteo_actualizados
            logger.info(f"Migración de teléfonos completada:")
            logger.info(f"- Teléfonos nuevos: {conteo_nuevos}")
            logger.info(f"- Teléfonos actualizados: {conteo_actualizados}")
            logger.info(f"- Total procesados: {self.conteo_migraciones['telefonos']}")
            return True

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error crítico al migrar teléfonos: {e}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return False

    def migrar_direcciones(self) -> bool:
        """Migra las direcciones de docentes."""
        conteo_nuevas = 0
        conteo_actualizadas = 0
        
        try:
            logger.info("Iniciando migración de direcciones de docentes...")
            
            # Verificar que hay datos para procesar
            if self.df_data is None or self.df_data.empty:
                logger.warning("No hay datos de docentes para procesar direcciones")
                return True  # No es un error, simplemente no hay datos
            
            for index, row in self.df_data.iterrows():
                try:
                    doc_id = self._validar_cedula(row.get('D_ID', ''))
                    if not doc_id or doc_id == "CEDULA_UN_DIGITO":
                        continue

                    # Buscar la persona en la base de datos
                    self.cursor.execute(
                        "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                        (doc_id,)
                    )
                    resultado = self.cursor.fetchone()
                    if not resultado:
                        logger.warning(f"No se encontró la persona con documento {doc_id} para migrar direcciones")
                        continue

                    persona_id = resultado[0]
                    direccion_completa = str(row.get('D_DIRECC', '')).strip()
                    
                    # Validar que la dirección no esté vacía y no sea un correo electrónico
                    if not direccion_completa or '@' in direccion_completa or direccion_completa.lower() in ['nan', 'none', 'null']:
                        continue

                    # Verificar si la dirección ya existe para esta persona
                    self.cursor.execute(
                        "SELECT id FROM direcciones WHERE persona_id = ? AND direccion_completa = ?",
                        (persona_id, direccion_completa)
                    )
                    dir_existe = self.cursor.fetchone()
                    
                    if dir_existe:
                        # Actualizar dirección existente
                        self.cursor.execute("""
                            UPDATE direcciones
                            SET tipo_direccion = ?, principal = ?
                            WHERE id = ?
                        """, ('residencia', 1, dir_existe[0]))
                        conteo_actualizadas += 1
                    else:
                        # Insertar nueva dirección
                        self.cursor.execute("""
                            INSERT INTO direcciones
                            (persona_id, estado, municipio, direccion_completa, tipo_direccion, principal)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (persona_id, '', '', direccion_completa, 'residencia', 1))
                        conteo_nuevas += 1

                    # Commit periódico
                    if (index + 1) % 50 == 0:
                        self.conn.commit()
                        logger.info(f"Procesadas direcciones para {index+1} docentes de {len(self.df_data)}...")

                except Exception as e:
                    logger.error(f"Error procesando direcciones del registro {index+1}: {e}")
                    continue

            self.conn.commit()
            self.conteo_migraciones['direcciones'] = conteo_nuevas + conteo_actualizadas
            logger.info(f"Migración de direcciones completada:")
            logger.info(f"- Direcciones nuevas: {conteo_nuevas}")
            logger.info(f"- Direcciones actualizadas: {conteo_actualizadas}")
            logger.info(f"- Total procesadas: {self.conteo_migraciones['direcciones']}")
            return True

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error crítico al migrar direcciones: {e}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return False

    def migrar_especifico(self) -> bool:
        """Migra la información específica de docentes."""
        return self.migrar_docentes()

    def migrar_docentes(self) -> bool:
        """Migra los datos específicos de docentes."""
        conteo_nuevos = 0
        conteo_actualizados = 0
        
        try:
            logger.info("Iniciando migración de información específica de docentes...")
            
            # Verificar que hay datos para procesar
            if self.df_data is None or self.df_data.empty:
                logger.warning("No hay datos de docentes para procesar información específica")
                return True  # No es un error, simplemente no hay datos
            
            for index, row in self.df_data.iterrows():
                try:
                    doc_id = self._validar_cedula(row.get('D_ID', ''))
                    if not doc_id or doc_id == "CEDULA_UN_DIGITO":
                        continue

                    # Buscar la persona en la base de datos
                    self.cursor.execute(
                        "SELECT id FROM informacion_personal WHERE documento_identidad = ?",
                        (doc_id,)
                    )
                    resultado = self.cursor.fetchone()
                    if not resultado:
                        logger.warning(f"No se encontró la persona con documento {doc_id} para migrar datos específicos")
                        continue

                    persona_id = resultado[0]
                    
                    # Procesar campos específicos de docentes
                    abreviatura_titulo = str(row.get('D_ABREVIA', '')).strip()
                    auxiliar_str = str(row.get('D_AUXILIAR', '')).strip().lower()
                    es_auxiliar = 1 if auxiliar_str in ['verdadero', 'true', '1', 'si', 'sí', 'yes'] else 0

                    # Verificar si el docente ya existe en la tabla docentes
                    self.cursor.execute(
                        "SELECT id FROM docentes WHERE persona_id = ?",
                        (persona_id,)
                    )
                    docente_existe = self.cursor.fetchone()

                    if docente_existe:
                        # Actualizar docente existente
                        self.cursor.execute("""
                            UPDATE docentes
                            SET abreviatura_titulo = ?, auxiliar = ?
                            WHERE persona_id = ?
                        """, (
                            abreviatura_titulo if abreviatura_titulo else None, 
                            es_auxiliar, 
                            persona_id
                        ))
                        conteo_actualizados += 1
                        logger.debug(f"Docente actualizado - Persona ID: {persona_id}")
                    else:
                        # Insertar nuevo docente
                        self.cursor.execute("""
                            INSERT INTO docentes (
                                persona_id, abreviatura_titulo, auxiliar
                            ) VALUES (?, ?, ?)
                        """, (
                            persona_id, 
                            abreviatura_titulo if abreviatura_titulo else None, 
                            es_auxiliar
                        ))
                        conteo_nuevos += 1
                        logger.debug(f"Docente insertado - Persona ID: {persona_id}")

                    # Commit cada 50 registros para evitar problemas de memoria
                    if (index + 1) % 50 == 0:
                        self.conn.commit()
                        logger.info(f"Procesados {index+1} docentes de {len(self.df_data)}...")

                except Exception as e:
                    logger.error(f"Error procesando datos específicos del registro {index+1}: {e}")
                    continue

            self.conn.commit()
            self.conteo_migraciones['docentes'] = conteo_nuevos + conteo_actualizados
            logger.info(f"Migración de datos específicos de docentes completada:")
            logger.info(f"- Docentes nuevos: {conteo_nuevos}")
            logger.info(f"- Docentes actualizados: {conteo_actualizados}")
            logger.info(f"- Total procesados: {self.conteo_migraciones['docentes']}")
            
            # Verificar que realmente se insertaron datos
            self.cursor.execute("SELECT COUNT(*) FROM docentes")
            total_docentes = self.cursor.fetchone()[0]
            logger.info(f"Total de docentes en la tabla docentes: {total_docentes}")
            
            return True

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error crítico al migrar datos específicos de docentes: {e}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
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
        
        # Crear directorio de reportes si no existe
        if not os.path.exists('reportes'):
            os.makedirs('reportes')
        
        # Función auxiliar para guardar con manejo de errores
        def guardar_archivo_json(datos, nombre_archivo, descripcion):
            try:
                # Verificar que los datos no estén vacíos
                if not datos:
                    logger.info(f"No hay {descripcion} para guardar")
                    return
                
                # Ruta completa del archivo
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
                    ruta_txt = os.path.join('reportes', nombre_txt)
                    with open(ruta_txt, "w", encoding="utf-8") as f:
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
                    logger.info(f"Archivo de respaldo creado: {ruta_txt}")
                except Exception as e2:
                    logger.error(f"Error al crear archivo de respaldo: {e2}")
        
        # Guardar cada tipo de registro con prefijo DCT
        if self.registros_cedula_vacia:
            archivo_vacias = f"DCT_registros_cedula_vacia_{timestamp}.json"
            guardar_archivo_json(self.registros_cedula_vacia, archivo_vacias, "Registros de docentes con cédula vacía")
        
        if self.registros_cedula_invalida:
            archivo_invalidas = f"DCT_registros_cedula_un_digito_{timestamp}.json"
            guardar_archivo_json(self.registros_cedula_invalida, archivo_invalidas, "Registros de docentes con cédula de un dígito")
        
        if self.registros_actualizados:
            archivo_actualizados = f"DCT_registros_actualizados_{timestamp}.json"
            guardar_archivo_json(self.registros_actualizados, archivo_actualizados, "Registros de docentes actualizados")

        # Mostrar resumen
        total_problematicos = len(self.registros_cedula_vacia) + len(self.registros_cedula_invalida)
        total_actualizados = len(self.registros_actualizados)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"RESUMEN DE REGISTROS ESPECIALES DOCENTES:")
        logger.info(f"{'='*60}")
        logger.info(f"- Cédulas vacías: {len(self.registros_cedula_vacia)}")
        logger.info(f"- Cédulas de un dígito: {len(self.registros_cedula_invalida)}")
        logger.info(f"- Registros actualizados: {len(self.registros_actualizados)}")
        logger.info(f"- Total registros problemáticos: {total_problematicos}")
        logger.info(f"{'='*60}")
