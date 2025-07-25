import tkinter.messagebox as messagebox
from models.Sedes.models_sedes import ModeloSedes
from datetime import datetime

class ControladorSedes:
    def __init__(self):
        self.modelo = ModeloSedes()

    def obtener_datos_vista(self, vista):

        dic_datos = {
            
            "codigo": vista.codigo_entry.get(),
            "nombre": vista.nombre_entry.get(),
            "nombre_corto": vista.nombre_corto_entry.get(),
            "tipo": vista.tipo_entry.get(),
            "direccion": vista.direccion_entry.get(),
            "telefono": vista.telefono_entry.get(),
            "correo": vista.correo_entry.get(),
            "director": vista.director_entry.get(),
            "coordinador_academico": vista.coordinador_academico_entry.get(),
            "estado": vista.estado_menu.get(),
            "observaciones": vista.observacion_entry.get()
        }

        return dic_datos
    
    def resgistrar_sede(self,datos,ventana):
        exito = self.modelo.registrar_sede(datos,self.obtener_fecha_actual)
        if exito:
            messagebox.showinfo("Éxito", "Sede registrada correctamente.", parent=ventana)
        else:
            messagebox.showerror("Error", "No se pudo registrar la sede.", parent=ventana)


    def obtener_fecha_actual(self):
        return datetime.now().strftime("%Y-%m-%d")
    
    def listar_sedes(self):
        return self.modelo.listar_sedes()
    
    def actualizar_sede(self, sede_id, datos_actualizados, ventana):
        exito = self.modelo.actualizar_sede(sede_id, datos_actualizados,self.obtener_fecha_actual())
        if exito:
            messagebox.showinfo("Éxito", "Datos de la sede actualizados correctamente.", parent=ventana)
            return True
        else:
            messagebox.showerror("Error", "No se pudo actualizar los datos de la sede.", parent=ventana)
            return False
        
    def obtener_codigos(self):
        return self.modelo.obtener_codigos()
    
    def obtener_id_por_codigo(self, codigo):
        return self.modelo.obtener_id_por_codigo(codigo)
    
    def obtener_nombres_por_id(self, tabla, id):
        return self.modelo.obtener_nombres_por_id(tabla, id)