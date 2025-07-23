import tkinter.messagebox as messagebox
from models.Secciones.models_secciones import ModeloSecciones


class ControllerSecciones:

    def __init__(self):
        self.modelo = ModeloSecciones()
    
    def obtener_datos_vista(self, vista):
        
        sede_id = vista.controller_sede.obtener_id_por_codigo(vista.var_sede.get())
        periodo_academico_id = vista.controller_PA.obtener_id_por_codigo(vista.var_periodo.get())

        for id_nombre in vista.id_nombres_docentes:
            if id_nombre[1] == vista.var_docente.get():
                docente_titular_id = id_nombre[0]
                break

        datos = {
            "sede_id": sede_id,
            "periodo_academico_id": periodo_academico_id,
            "codigo_seccion": vista.codigo_entry.get(),
            "docente_titular_id": docente_titular_id,
            "cupo_maximo": vista.cupo_maximo_entry.get(),
            "turno": vista.var_turno.get(),
            "modalidad": vista.var_modalidad.get(),
            "aula": vista.aula_entry.get(),
            "estado": vista.var_estado.get(),
            "pnf_id": vista.pnf_id_por_nombre[vista.var1.get()],
            "trayecto_id": vista.trayecto_id_por_nombre[vista.var_trayecto.get()],
            "tramo_id": vista.tramo_id_por_nombre[vista.var_tramo.get()]
        }
        return datos
    
    def campos_obligatorios(self, vista, datos):
       
        alias=[
            ("codigo_seccion", "Codigo"),
            ("cupo_maximo", "Cupo Máximo"),
            ("aula", "Aula")
        ]

        for campo,nombre_mostrar in alias:
            if datos[campo] == "" or datos[campo] == None:
                messagebox.showwarning("Campo Vacío", f"El campo '{nombre_mostrar}' es obligatorio.", parent=vista)
                return False
        return True
        
    def registrar_seccion(self,datos, vista):
        exito = self.modelo.registrar_sede(datos)

        if exito:
            messagebox.showinfo(title="Exito",message="Se registro la seccion correctamente", parent=vista)
            return True
        else:
            messagebox.showerror(title="Error",message="No se pudo registrar la seccion", parent=vista)
            return False
        

    def limpiar_formulario_completo(self, vista):
        pass