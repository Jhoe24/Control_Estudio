import tkinter.messagebox as messagebox

from models.Docentes.RegistroDocentes import ModeloDocente

class DocenteController:
    def __init__(self):
        self.modelo_docente = ModeloDocente()

    def registrar_docente(self, dic_docentes, vista_formulario):
        
        resultado = self.modelo_docente.registrar_docente(dic_docentes)
        if resultado:
            messagebox.showinfo("Registro Exitoso", "El docente ha sido registrado exitosamente.", parent=vista_formulario)
            self.limpiar_formulario_completo(vista_formulario)
        else:
            messagebox.showerror("Error de Registro", "No se pudo registrar el docente. Por favor, intente nuevamente.", parent=vista_formulario)
        print(dic_docentes)
        
    def obtener_lista_docentes(self,desde=0):
        #Obtener 10 registro de docentes
        nmin = 0
        nmax = self.modelo_docente.obtener_id_ultimo()
        if nmax == None:
            return []
        if desde < nmin : desde = nmin
        if desde > (nmax) : desde = nmax-1
        resultado = self.modelo_docente.lista_Docentes(desde)
        # print(resultado)
        return resultado

    def cargar_docente_edicion(self,id,datos,ventana):
        resultado = self.modelo_docente.update_docente(id,datos)

        if resultado:
            messagebox.showinfo("Info", "Exito al actualizar los datos del docente")
            return True
        else:
            messagebox.showerror("Error", "Hubo un error al actualizar los datos del docente.", parent=ventana)
            return False
        #print(f"id: {id} '/n Datos: {datos}")

    def buscar_estudiante(self, tipo_doc, nro_doc):
        
        registro = self.modelo_docente.buscar_estudiante(tipo_doc, nro_doc)

        if registro:
            return registro
        else:
            messagebox.showerror("Error", "No se encontró el docente con los datos proporcionados.")
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

    def obtener_solo_nombres_docentes_por_pnf(self, pnf_id):
        dic_nombres = self.modelo_docente.obtener_nombres_docentes(pnf_id)
        nombres = []
        
        for dic_doc in dic_nombres:
            nombres.append((dic_doc["id"],dic_doc["nombres"]+" "+dic_doc["apellidos"]))
            
        return nombres

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
            "lista_telefonos": telefonos,
            
            #Datos del docente

            "abreviatura_titulo": vista_formulario.datos_docente_frame.abreviatura_menu.get(),
            "especialidad": vista_formulario.datos_docente_frame.especialidad_entry.get(),
            "fecha_ingreso": vista_formulario.datos_docente_frame.fecha_ingreso_entry.get(), #comentarle de esto a andy
            "tipo_contrato": vista_formulario.datos_docente_frame.tipo_contrato_menu.get(),
            "categoria": vista_formulario.datos_docente_frame.categoria_entry.get(),
            "auxiliar": vista_formulario.datos_docente_frame.auxiliar_menu.get(),
            "dedicacion": vista_formulario.datos_docente_frame.dedicacion_menu.get(),
            "estado_doc": vista_formulario.datos_docente_frame.estado_doc_menu.get(),  
            

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
            vista_formulario.datos_docente_frame.especialidad_entry,
            vista_formulario.datos_docente_frame.fecha_ingreso_entry, #comentarle de esto a andy
            vista_formulario.datos_docente_frame.categoria_entry,
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
            vista_formulario.datos_docente_frame.abreviatura_menu: "Prof.",
            vista_formulario.datos_docente_frame.tipo_contrato_menu: "Tiempo completo",
            vista_formulario.datos_docente_frame.auxiliar_menu: "Si",
            vista_formulario.datos_docente_frame.dedicacion_menu: "Exclusiva",
            vista_formulario.datos_docente_frame.estado_doc_menu: "Activo",
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

        #vista_formulario.datos_personales_frame.tipo_documento_var.set("Cédula")
        #vista_formulario.datos_personales_frame._actualizar_estado_nro_doc()

        # if vista_formulario.datos_personales_frame.tipo_documento_var.get() != "Sin Documento":
        #     vista_formulario.datos_personales_frame.nro_documento_entry.focus_set()
        #     vista_formulario.datos_personales_frame.nro_documento_entry.configure(state = "normal")
        # else:
        #     if vista_formulario.datos_personales_frame.nombre_entry:
        #         vista_formulario.datos_personales_frame.nombre_entry.focus_set()
        vista_formulario.datos_personales_frame.nro_documento_entry.focus_set()
        vista_formulario.datos_personales_frame.nro_documento_entry.configure(state="normal")
