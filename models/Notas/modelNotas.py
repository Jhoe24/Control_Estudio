import sqlite3 as sql
import os
from datetime import date
from pprint import pprint

class ModeloNotas:
    def __init__(self):
       self.db_ruta = os.path.join('db', 'sistema_academico.db')

    def is_assigned_pnf(self, estudiante_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('''
                            SELECT pnf_id, trayecto_actual FROM estudiante_pnf WHERE estudiante_id = ?
                            ''',(estudiante_id,))
            resultado = cursor.fetchone()
            con.close()
            if resultado:
                return resultado
            else:
                return False
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
        
    def failed_project(self, estudiante_id, pnf_id, trayecto_actual):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            """
            1. Obtener todas la Unidades Curriculares 
            """
           
            con.close()
            
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

            
#print(ModeloNotas().is_assigned_pnf(11))