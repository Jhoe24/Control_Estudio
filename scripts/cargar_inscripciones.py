import sqlite3
import os

inscripciones_data = [
    {"estudiante_id": 10, "seccion_id": 1},
    {"estudiante_id": 9, "seccion_id": 1},
    {"estudiante_id": 8, "seccion_id": 1},
    {"estudiante_id": 7, "seccion_id": 1},
    {"estudiante_id": 6, "seccion_id": 2},
    {"estudiante_id": 4, "seccion_id": 2},
    {"estudiante_id": 3, "seccion_id": 2},
    {"estudiante_id": 2, "seccion_id": 2},
]

class CargadorInscripciones:
    def __init__(self, inscripciones_data, db_path=None):
        self.inscripciones_data = inscripciones_data
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', 'db', 'sistema_academico.db')
        self.con = None

    def conectar(self):
        """Abre conexión SQLite con FK habilitadas."""
        self.con = sqlite3.connect(self.db_path)
        self.con.execute("PRAGMA foreign_keys = ON;")

    def cerrar(self):
        """Cierra la conexión."""
        if self.con:
            self.con.close()

    def insertar_inscripcion(self, insc):
        """Inserta una inscripción en la tabla inscripciones."""
        if not self.con:
            raise ConnectionError("Conexión no establecida.")

        sql = '''
        INSERT OR IGNORE INTO inscripciones (
            estudiante_id, seccion_id,
            fecha_inscripcion, condicion, estado
        ) VALUES (
            ?, ?, CURRENT_DATE, 'Regular', 'Inscrito'
        )
        '''
        params = (insc['estudiante_id'], insc['seccion_id'])

        try:
            cur = self.con.cursor()
            cur.execute(sql, params)
            self.con.commit()
            if cur.rowcount:
                print(f"✅ Inscripción: estudiante {insc['estudiante_id']} → sección {insc['seccion_id']} (ID: {cur.lastrowid}).")
            else:
                print(f"ℹ️  Ya existía inscripción de estudiante {insc['estudiante_id']} en sección {insc['seccion_id']}.")
        except sqlite3.IntegrityError as e:
            print(f"❌ Error de integridad al inscribir estudiante {insc['estudiante_id']} en sección {insc['seccion_id']}: {e}")
            self.con.rollback()
        except Exception as e:
            print(f"❌ Error insertando inscripción {insc}: {e}")
            self.con.rollback()
            raise

    def cargar(self):
        """Carga todas las inscripciones definidas en inscripciones_data."""
        if not os.path.exists(self.db_path):
            print(f"Error: base de datos no encontrada en '{self.db_path}'.")
            print("Ejecuta primero 'creacion_db.py'.")
            return

        try:
            self.conectar()
            print("="*50)
            print("Iniciando carga masiva de inscripciones...")
            print("="*50)
            for insc in self.inscripciones_data:
                self.insertar_inscripcion(insc)
            print("\nCarga de inscripciones finalizada.")
            print("="*50)
        finally:
            self.cerrar()

if __name__ == "__main__":
    cargador = CargadorInscripciones(inscripciones_data)
    cargador.cargar()
