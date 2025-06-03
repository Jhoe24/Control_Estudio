
import tkinter.messagebox as messagebox

from models.RegistroEstudiantes import RegistroEstudiantes

class EstudianteController:
    def __init__(self):
        self.modelo = RegistroEstudiantes()

    def procesar_guardado_estudiante(self, datos_estudiante, vista_formulario):
        """
        Procesa la solicitud de guardar (crear o actualizar) un estudiante.
        Este método será llamado desde FormularioEstudianteView.

        Args:
            datos_estudiante (dict): Un diccionario con todos los datos del formulario.
            vista_formulario (FormularioEstudianteView): La instancia de la vista del formulario,
                                                        para poder interactuar con ella (ej. mostrar errores específicos).
        """
    
        # registrar estudiantes en la base de datos
        # funcion de procesar_guardado_de_datos
        exito = self.modelo.registrar_estudiante(datos_estudiante)
        
        if exito:
            messagebox.showinfo("Info", "Exito al registrar al nuevo estudiante")
            return True
        else:
            messagebox.showerror("Error", "Hubo un error al registrar el estudiante.", parent=vista_formulario)
            return False
        print(datos_estudiante)

    def cargar_estudiante_para_edicion(self, id_estudiante, dic_estudiante, vista_formulario):
        existo = self.modelo.update_estudiante(id_estudiante, dic_estudiante)
        if existo:
            messagebox.showinfo("Info", "Exito al actualizar los datos del estudiante")
            return True
        else:
            messagebox.showerror("Error", "Hubo un error al actualizar los datos del estudiante.", parent=vista_formulario)
            return False

    def obtener_lista_estudiantes(self,desde):
        #Obtener 10 registro de estudiantes
        nmin = 0
        nmax = self.modelo.obtener_id_ultimo()
        if desde < nmin : desde = nmin
        if desde > (nmax) : desde = nmax-1
        resultado = self.modelo.lista_Estudiantes(desde)
        return resultado

    def buscar_estudiante(self, tipo_doc, nro_doc):
        
        registro = self.modelo.buscar_estudiante(tipo_doc, nro_doc)

        if registro:
            return registro
        else:
            messagebox.showerror("Error", "No se encontró el estudiante con los datos proporcionados.")
            return None


    def _solo_numeros(self, char_input):
        return char_input.isdigit()

    def _numeros_y_barras(self, char_input):
        return char_input.isdigit() or char_input in "-/"

    def _solo_decimal(self, valor_actual, char_input):
        if char_input in "0123456789":
            return True
        if char_input == "." and "." not in valor_actual:
            return True
        if char_input == "":
            return True  # Permitir borrar
        return False

    def validar_campos_obligatorios(self, datos_estudiante, vista_formulario):
        try:
                
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
                #("telefono_principal", "Teléfono Principal"),
                ("condicion", "Condición"),
                #("institucion", "Institución"),
                #("titulo_obtenido", "Título Obtenido"),
                #("f_grado", "Fecha Grado"),
                #("promedio_bachiller", "Promedio Bachillerato"),
                #("codigo_sni", "Código SNI"),
                #("anio_sni", "Año SNI"),
                #("estado", "Estado"),
                #("municipio", "Municipio"),
                #("parroquia", "Parroquia"),
                #("sector", "Sector"),
                #("calle", "Calle"),
                #("casa_apart", "Casa o Apartamento"),
                
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
        
        except Exception as e:
            print(e)

    def obtener_todos_los_datos(self, vista_formulario):
        # Extrae los teléfonos de la vista dinámica
        # telefonos = [
        #     {
        #         "tipo": tel[1].get(),
        #         "numero": tel[3].get()
        #     }
        #     for tel in vista_formulario.datos_personales_frame.telefono_widgets
        #     if tel[3].get().strip()
        # ]
        telefonos = vista_formulario.datos_personales_frame.obtener_telefonos()

        datos = {
            "tipo_documento": vista_formulario.datos_personales_frame.tipo_documento_var.get(),
            "nro_documento": vista_formulario.datos_personales_frame.nro_documento_entry.get(),
            "nombre": vista_formulario.datos_personales_frame.nombre_entry.get(),
            "apellido": vista_formulario.datos_personales_frame.apellido_entry.get(),
            "nacionalidad": vista_formulario.datos_personales_frame.nacionalidad_menu.get(),
            "genero": vista_formulario.datos_personales_frame.genero_menu.get(),
            "edo_civil": vista_formulario.datos_personales_frame.edo_civil_menu.get(),
            "f_nacimiento": vista_formulario.datos_personales_frame.fnac_entry.get(),
            "lugar_nacimiento": vista_formulario.datos_personales_frame.lugar_nac_entry.get(),
            "f_ingreso": vista_formulario.datos_personales_frame.fingreso_entry.get(),
            "correo_electronico": vista_formulario.datos_personales_frame.correo_electronico_entry.get(),
            # "tipo_telefono_p": telefonos[0]["tipo"] if len(telefonos) > 0 else "",
            # "telefono_principal": telefonos[0]["numero"] if len(telefonos) > 0 else "",
            # "tipo_telefono_s": telefonos[1]["tipo"] if len(telefonos) > 1 else "",
            # "telefono_secundario": telefonos[1]["numero"] if len(telefonos) > 1 else "",
            "lista_telefonos": telefonos,
            "condicion": vista_formulario.informacion_academica_frame.condicion_menu.get(),
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
            "casa_apart": vista_formulario.datos_ubicacion_frame.casa_apart_entry.get(),
            "tipo_direccion": vista_formulario.datos_ubicacion_frame.tipo_direccion_menu.get()
        }
        return datos

    def limpiar_formulario_completo(self, vista_formulario):
        entries_a_limpiar = [
            vista_formulario.datos_personales_frame.nro_documento_entry,
            vista_formulario.datos_personales_frame.nombre_entry,
            vista_formulario.datos_personales_frame.apellido_entry,
            vista_formulario.datos_personales_frame.fnac_entry,
            vista_formulario.datos_personales_frame.lugar_nac_entry,
            vista_formulario.datos_personales_frame.fingreso_entry,
            vista_formulario.datos_personales_frame.correo_electronico_entry,
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
            vista_formulario.datos_personales_frame.genero_menu: "M",
            vista_formulario.datos_personales_frame.edo_civil_menu: "Soltero",
            vista_formulario.datos_personales_frame.nacionalidad_menu: "Venezolano",
            vista_formulario.informacion_academica_frame.tipo_inst_menu: "Pública",
            vista_formulario.informacion_academica_frame.condicion_menu: "Regular",
            vista_formulario.datos_ubicacion_frame.tipo_direccion_menu: "residencia",
        }

        for entry in entries_a_limpiar:
            if hasattr(entry, 'delete'):
                entry.delete(0, 'end')
        for menu, valor in option_menus_a_resetear.items():
            if hasattr(menu, 'set'):
                menu.set(valor)

        # Limpiar los campos de teléfono
        vista_formulario.datos_personales_frame.limpiar_telefonos()

        # vista_formulario.datos_personales_frame.tipo_documento_var.set("Cédula")
        # vista_formulario.datos_personales_frame._actualizar_estado_nro_doc()

        # if vista_formulario.datos_personales_frame.tipo_documento_var.get() != "Sin Documento":
        #     vista_formulario.datos_personales_frame.nro_documento_entry.focus_set()
        # else:
        #     if vista_formulario.datos_personales_frame.nombre_entry:
        #         vista_formulario.datos_personales_frame.nombre_entry.focus_set()
        vista_formulario.datos_personales_frame.nro_documento_entry.focus_set()
        vista_formulario.datos_personales_frame.nro_documento_entry.configure(state="normal")
