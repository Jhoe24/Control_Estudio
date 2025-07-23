import sqlite3
import os

notas_data = [
    {"inscripcion_id": 1, "unidad_curricular_id": 5, "valor": 18.5},
    {"inscripcion_id": 2, "unidad_curricular_id": 5, "valor": 16.0},
    {"inscripcion_id": 3, "unidad_curricular_id": 5, "valor": 12.75},
    {"inscripcion_id": 4, "unidad_curricular_id": 6, "valor": 14.0},
    {"inscripcion_id": 5, "unidad_curricular_id": 6, "valor": 19.0},
    {"inscripcion_id": 6, "unidad_curricular_id": 7, "valor": 10.5},
    {"inscripcion_id": 7, "unidad_curricular_id": 7, "valor": 13.25},
    {"inscripcion_id": 8, "unidad_curricular_id": 8, "valor": 17.0},
]

class CargadorNotas:
    def __init__(self, notas_data, db_path=None):
        self.notas_data = notas_data
        # ruta por defecto ../db/sistema_academico.db
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', 'db', 'sistema_academico.db')
        self.con = None

    def conectar(self):
        """Abre conexión SQLite con foreign keys habilitadas."""
        self.con = sqlite3.connect(self.db_path)
        self.con.execute("PRAGMA foreign_keys = ON;")

    def cerrar(self):
        """Cierra la conexión."""
        if self.con:
            self.con.close()

    def insertar_nota(self, nota):
        """Inserta o actualiza una nota final en la tabla notas."""
        if not self.con:
            raise ConnectionError("Conexión no establecida.")

        sql = '''
        INSERT OR REPLACE INTO notas (
            inscripcion_id,
            unidad_curricular_id,
            valor,
            fecha_registro
        ) VALUES (
            ?, ?, ?, CURRENT_TIMESTAMP
        )
        '''
        params = (
            nota['inscripcion_id'],
            nota['unidad_curricular_id'],
            nota['valor']
        )

        try:
            cur = self.con.cursor()
            cur.execute(sql, params)
            self.con.commit()
            action = "Insertada" if cur.rowcount else "Actualizada"
            print(f"✅ Nota {action}: inscripción {nota['inscripcion_id']}, UC {nota['unidad_curricular_id']} → {nota['valor']}")
        except sqlite3.IntegrityError as e:
            print(f"❌ Error de integridad al guardar nota (insc {nota['inscripcion_id']}, UC {nota['unidad_curricular_id']}): {e}")
            self.con.rollback()
        except Exception as e:
            print(f"❌ Error insertando nota {nota}: {e}")
            self.con.rollback()
            raise

    def cargar(self):
        """Carga todas las notas definidas en notas_data."""
        if not os.path.exists(self.db_path):
            print(f"Error: base de datos no encontrada en '{self.db_path}'.")
            print("Ejecuta primero 'creacion_db.py'.")
            return

        try:
            self.conectar()
            print("="*50)
            print("Iniciando carga masiva de notas finales...")
            print("="*50)
            for nota in self.notas_data:
                self.insertar_nota(nota)
            print("\nCarga de notas finalizada.")
            print("="*50)
        finally:
            self.cerrar()

if __name__ == "__main__":
    cargador = CargadorNotas(notas_data)
    cargador.cargar()
