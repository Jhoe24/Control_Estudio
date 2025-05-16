import tkinter.messagebox as messagebox

class EstudianteController:
    def __init__(self, modelo):
        pass

    def procesar_guardado_estudiante(self, datos_estudiante, vista_formulario):
        """
        Procesa la solicitud de guardar (crear o actualizar) un estudiante.
        Este método será llamado desde FormularioEstudianteView.

        Args:
            datos_estudiante (dict): Un diccionario con todos los datos del formulario.
            vista_formulario (FormularioEstudianteView): La instancia de la vista del formulario,
                                                        para poder interactuar con ella (ej. mostrar errores específicos).
        """
        print(f"DEBUG: EstudianteController - Recibidos datos para guardar: {datos_estudiante}")

        # Simulación de éxito
        print(f"INFO: EstudianteController - Procesamiento de guardado para {datos_estudiante['nombre']} finalizado (simulación).")
        return True  # Indica éxito a la vista para que pueda reaccionar (ej. limpiar campos)

    def cargar_estudiante_para_edicion(self, id_estudiante, vista_formulario):
        """
        Carga los datos de un estudiante por su ID y le dice a la vista que llene los campos.
        (Esta función es para cuando tengas una lista de estudiantes y selecciones uno para editar)

        Args:
            id_estudiante: El ID del estudiante a cargar.
            vista_formulario (FormularioEstudianteView): La instancia de la vista.
        """
        print(f"DEBUG: EstudianteController - Solicitud para cargar estudiante ID: {id_estudiante}")
        pass  # Implementar cuando tengas la lista y el modelo

    def obtener_lista_estudiantes(self, criterios_busqueda=None):
        """
        Obtiene una lista de estudiantes del modelo, posiblemente filtrada.
        (Para una vista que muestre una tabla de estudiantes)

        Args:
            criterios_busqueda (dict, optional): Diccionario con criterios para filtrar. Defaults to None.

        Returns:
            list: Lista de objetos/diccionarios de estudiantes.
        """
        print(f"DEBUG: EstudianteController - Obteniendo lista de estudiantes. Criterios: {criterios_busqueda}")
        return []  # Simulación

    def _solo_numeros(self, char_input):
        return char_input.isdigit()

    def _numeros_y_barras(self, char_input):
        return char_input.isdigit() or char_input == '/'

    def _solo_decimal(self, valor_actual, char_input):
        if char_input in "0123456789":
            return True
        if char_input == "." and "." not in valor_actual:
            return True
        if char_input == "":
            return True  # Permitir borrar
        return False

    def validar_campos_obligatorios(self, datos_estudiante, vista_formulario):
        tipo_doc_seleccionado = datos_estudiante.get("tipo_documento")
        nro_doc_valor = datos_estudiante.get("nro_documento", "").strip()

        if tipo_doc_seleccionado == "Cédula":
            if not nro_doc_valor:
                messagebox.showwarning("Campo Vacío", "El campo 'Nro. Cédula' es obligatorio.", parent=vista_formulario)
                return False
        elif tipo_doc_seleccionado == "Pasaporte":
            if not nro_doc_valor:
                messagebox.showwarning("Campo Vacío", "El campo 'Nro. Pasaporte' es obligatorio.", parent=vista_formulario)
                return False

        campos_a_validar = [
            ("nombre", "Nombre"),
            ("apellido", "Apellido"),
            ("nacionalidad", "Nacionalidad"),
            ("f_nacimiento", "Fecha de Nacimiento"),
            ("lugar_nacimiento", "Lugar de Nacimiento"),
            ("f_ingreso", "Fecha de Ingreso"),
            ("correo_electronico", "Correo Electrónico"),
            ("telefono_principal", "Teléfono Principal"),
            ("condicion", "Condición"),
            ("institucion", "Institución"),
            ("titulo_obtenido", "Título Obtenido"),
            ("f_grado", "Fecha Grado"),
            ("promedio_bachiller", "Promedio Bachillerato"),
            ("codigo_sni", "Código SNI"),
            ("anio_sni", "Año SNI"),
            ("estado", "Estado"),
            ("municipio", "Municipio"),
            ("parroquia", "Parroquia"),
            ("sector", "Sector"),
            ("calle", "Calle"),
            ("casa_apart", "Casa o Apartamento"),
        ]

        for campo, nombre_campo in campos_a_validar:
            valor_campo = datos_estudiante.get(campo, "").strip()

            if nombre_campo == "Correo Electrónico" and valor_campo:
                if "@" not in valor_campo or "." not in valor_campo.split("@")[-1] or len(valor_campo.split("@")[-1].split(".")[-1]) < 2:
                    messagebox.showwarning("Campo Inválido", f"El formato del '{nombre_campo}' no es válido.", parent=vista_formulario)
                    return False

            if not valor_campo:
                messagebox.showwarning("Campo Vacío", f"El campo '{nombre_campo}' es obligatorio.", parent=vista_formulario)
                return False

        return True

    def obtener_todos_los_datos(self, vista_formulario):
        datos = {
            "tipo_documento": vista_formulario.datos_personales_frame.tipo_documento_var.get(),
            "nro_documento": vista_formulario.datos_personales_frame.nro_documento_entry.get(),
            "nombre": vista_formulario.datos_personales_frame.nombre_entry.get(),
            "apellido": vista_formulario.datos_personales_frame.apellido_entry.get(),
            "genero": vista_formulario.datos_personales_frame.genero_menu.get(),
            "edo_civil": vista_formulario.datos_personales_frame.edo_civil_menu.get(),
            "nacionalidad": vista_formulario.datos_personales_frame.nacionalidad_entry.get(),
            "f_nacimiento": vista_formulario.datos_personales_frame.fnac_entry.get(),
            "lugar_nacimiento": vista_formulario.datos_personales_frame.lugar_nac_entry.get(),
            "f_ingreso": vista_formulario.datos_personales_frame.fingreso_entry.get(),
            "correo_electronico": vista_formulario.datos_personales_frame.correo_electronico_entry.get(),
            "telefono_principal": vista_formulario.datos_personales_frame.telefono_principal_entry.get(),
            "telefono_secundario": vista_formulario.datos_personales_frame.telefono_secundario_entry.get(),
            "condicion": vista_formulario.datos_personales_frame.condicion_menu.get(),
            "tipo_institucion": vista_formulario.informacion_academica_frame.tipo_inst_menu.get(),
            "institucion": vista_formulario.informacion_academica_frame.institucion_entry.get(),
            "titulo_obtenido": vista_formulario.informacion_academica_frame.titulo_entry.get(),
            "promedio_bachiller": vista_formulario.informacion_academica_frame.promedio_entry.get(),
            "f_grado": vista_formulario.informacion_academica_frame.fgrado_entry.get(),
            "codigo_sni": vista_formulario.sistema_ingreso_frame.codigo_entry.get(),
            "anio_sni": vista_formulario.sistema_ingreso_frame.anio_entry.get(),
            "estado": vista_formulario.datos_ubicacion_frame.estado_entry.get(),
            "municipio": vista_formulario.datos_ubicacion_frame.municipio_entry.get(),
            "parroquia": vista_formulario.datos_ubicacion_frame.parroquia_entry.get(),
            "sector": vista_formulario.datos_ubicacion_frame.sector_entry.get(),
            "calle": vista_formulario.datos_ubicacion_frame.calle_entry.get(),
            "casa_apart": vista_formulario.datos_ubicacion_frame.casa_apart_entry.get()
        }
        return datos

    def limpiar_formulario_completo(self, vista_formulario):
        entries_a_limpiar = [
            vista_formulario.datos_personales_frame.nro_documento_entry,
            vista_formulario.datos_personales_frame.nombre_entry,
            vista_formulario.datos_personales_frame.apellido_entry,
            vista_formulario.datos_personales_frame.nacionalidad_entry,
            vista_formulario.datos_personales_frame.fnac_entry,
            vista_formulario.datos_personales_frame.lugar_nac_entry,
            vista_formulario.datos_personales_frame.fingreso_entry,
            vista_formulario.datos_personales_frame.correo_electronico_entry,
            vista_formulario.datos_personales_frame.telefono_principal_entry,
            vista_formulario.datos_personales_frame.telefono_secundario_entry,
            vista_formulario.informacion_academica_frame.institucion_entry,
            vista_formulario.informacion_academica_frame.titulo_entry,
            vista_formulario.informacion_academica_frame.fgrado_entry,
            vista_formulario.informacion_academica_frame.promedio_entry,
            vista_formulario.sistema_ingreso_frame.codigo_entry,
            vista_formulario.sistema_ingreso_frame.anio_entry,
            vista_formulario.datos_ubicacion_frame.estado_entry,
            vista_formulario.datos_ubicacion_frame.municipio_entry,
            vista_formulario.datos_ubicacion_frame.parroquia_entry,
            vista_formulario.datos_ubicacion_frame.sector_entry,
            vista_formulario.datos_ubicacion_frame.calle_entry,
            vista_formulario.datos_ubicacion_frame.casa_apart_entry,
        ]
        option_menus_a_resetear = {
            vista_formulario.datos_personales_frame.genero_menu: "Masculino",
            vista_formulario.datos_personales_frame.edo_civil_menu: "Soltero",
            vista_formulario.informacion_academica_frame.tipo_inst_menu: "Pública"
        }

        for entry in entries_a_limpiar:
            if hasattr(entry, 'delete'):
                entry.delete(0, 'end')
        for menu, valor in option_menus_a_resetear.items():
            if hasattr(menu, 'set'):
                menu.set(valor)

        vista_formulario.datos_personales_frame.tipo_documento_var.set("Cédula")
        vista_formulario.datos_personales_frame._actualizar_estado_nro_doc()

        if vista_formulario.datos_personales_frame.tipo_documento_var.get() != "Sin Documento":
            vista_formulario.datos_personales_frame.nro_documento_entry.focus_set()
        else:
            if vista_formulario.datos_personales_frame.nombre_entry:
                vista_formulario.datos_personales_frame.nombre_entry.focus_set()
