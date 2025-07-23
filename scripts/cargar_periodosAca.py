import sqlite3
import os

periodos_data = [
    {
        "codigo": "2025-1",
        "nombre": "Primer Semestre 2025",
        "tipo": "Regular",
        "fecha_inicio": "2025-01-15",
        "fecha_fin": "2025-06-15",
        "fecha_inicio_inscripcion": "2024-12-01",
        "fecha_fin_inscripcion": "2025-01-10",
        "fecha_inicio_clases": "2025-01-15",
        "fecha_fin_clases": "2025-05-30",
        "fecha_inicio_evaluaciones": "2025-06-01",
        "fecha_fin_evaluaciones": "2025-06-15",
        "duracion_semanas": 22,
        "estado": "planificacion",
        "observaciones": "Semestre inicial del año 2025"
    },
    {
        "codigo": "2025-2",
        "nombre": "Segundo Semestre 2025",
        "tipo": "Regular",
        "fecha_inicio": "2025-08-01",
        "fecha_fin": "2025-12-20",
        "fecha_inicio_inscripcion": "2025-06-01",
        "fecha_fin_inscripcion": "2025-07-25",
        "fecha_inicio_clases": "2025-08-01",
        "fecha_fin_clases": "2025-12-05",
        "fecha_inicio_evaluaciones": "2025-12-10",
        "fecha_fin_evaluaciones": "2025-12-20",
        "duracion_semanas": 20,
        "estado": "planificacion",
        "observaciones": "Semestre vespertino 2025"
    },
    # Agrega más periodos según necesites...
]

class CargadorPeriodos:
    def __init__(self, periodos_data, db_path=None):
        self.periodos_data = periodos_data
        # Por defecto busca la DB en ../db/sistema_academico.db
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', 'db', 'sistema_academico.db')
        self.con = None

    def conectar(self):
        """Establece una conexión SQLite con FK habilitadas."""
        self.con = sqlite3.connect(self.db_path)
        self.con.execute("PRAGMA foreign_keys = ON;")

    def cerrar(self):
        """Cierra la conexión a la base de datos."""
        if self.con:
            self.con.close()

    def insertar_periodo(self, periodo):
        """Inserta un periodo académico en la tabla periodos_academicos."""
        if not self.con:
            raise ConnectionError("La conexión a la base de datos no está establecida.")

        sql = '''
            INSERT OR IGNORE INTO periodos_academicos (
                codigo, nombre, tipo,
                fecha_inicio, fecha_fin,
                fecha_inicio_inscripcion, fecha_fin_inscripcion,
                fecha_inicio_clases, fecha_fin_clases,
                fecha_inicio_evaluaciones, fecha_fin_evaluaciones,
                duracion_semanas, estado, observaciones
            ) VALUES (
                ?, ?, ?,
                ?, ?,
                ?, ?,
                ?, ?,
                ?, ?,
                ?, ?, ?
            )
        '''
        params = (
            periodo['codigo'], periodo['nombre'], periodo.get('tipo', 'Regular'),
            periodo['fecha_inicio'], periodo['fecha_fin'],
            periodo['fecha_inicio_inscripcion'], periodo['fecha_fin_inscripcion'],
            periodo['fecha_inicio_clases'], periodo['fecha_fin_clases'],
            periodo['fecha_inicio_evaluaciones'], periodo['fecha_fin_evaluaciones'],
            periodo.get('duracion_semanas'), periodo.get('estado', 'planificacion'),
            periodo.get('observaciones')
        )

        try:
            cur = self.con.cursor()
            cur.execute(sql, params)
            self.con.commit()
            if cur.rowcount:
                print(f"✅ Periodo '{periodo['codigo']} - {periodo['nombre']}' insertado.")
            else:
                print(f"ℹ️  Periodo '{periodo['codigo']}' ya existía. Se ignoró.")
        except sqlite3.IntegrityError as e:
            print(f"❌ Error de integridad al insertar periodo {periodo['codigo']}: {e}")
            self.con.rollback()
        except Exception as e:
            print(f"❌ Error insertando periodo {periodo['codigo']}: {e}")
            self.con.rollback()
            raise

    def cargar(self):
        """Carga todos los periodos definidos en periodos_data."""
        if not os.path.exists(self.db_path):
            print(f"Error: La base de datos en '{self.db_path}' no existe.")
            print("Ejecuta primero 'creacion_db.py'.")
            return

        try:
            self.conectar()
            print("="*50)
            print("Iniciando carga masiva de periodos académicos...")
            print("="*50)
            for periodo in self.periodos_data:
                self.insertar_periodo(periodo)
            print("\nCarga de periodos finalizada.")
            print("="*50)
        finally:
            self.cerrar()

if __name__ == "__main__":
    cargador = CargadorPeriodos(periodos_data)
    cargador.cargar()
