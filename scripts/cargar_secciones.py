import sqlite3
import os

secciones_data = [
    {
        "sede_id": 1,
        "periodo_academico_id": 1,
        "pnf_id": 1,
        "trayecto_id": 1,
        "tramo_id": 1,
        "codigo_seccion": "A1-2025-1",
        "docente_titular_id": 2,
        "docente_auxiliar_id": None,
        "cupo_maximo": 30,
        "cupo_minimo": 10,
        "turno": "Diurno",
        "modalidad": "Presencial",
        "aula": "101",
        "horario": "08:00-10:00",
        "dias_semana": "Lun,Mié,Vie",
        "fecha_inicio": "2025-01-15",
        "fecha_fin": "2025-05-30",
        "estado": "Planificada",
        "observaciones": "Sección piloto grupo A1"
    },
    {
        "sede_id": 1,
        "periodo_academico_id": 1,
        "pnf_id": 1,
        "trayecto_id": 1,
        "tramo_id": 1,
        "codigo_seccion": "B1-2025-1",
        "docente_titular_id": 3,
        "docente_auxiliar_id": 4,
        "cupo_maximo": 25,
        "cupo_minimo": 8,
        "turno": "Nocturno",
        "modalidad": "Semipresencial",
        "aula": "202",
        "horario": "18:00-20:00",
        "dias_semana": "Mar,Jue",
        "fecha_inicio": "2025-01-15",
        "fecha_fin": "2025-05-30",
        "estado": "Planificada",
        "observaciones": None
    },
]

class CargadorSecciones:
    def __init__(self, secciones_data, db_path=None):
        self.secciones_data = secciones_data
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', 'db', 'sistema_academico.db')
        self.con = None

    def conectar(self):
        """Establece conexión SQLite con foreign keys habilitadas."""
        self.con = sqlite3.connect(self.db_path)
        self.con.execute("PRAGMA foreign_keys = ON;")

    def cerrar(self):
        """Cierra la conexión."""
        if self.con:
            self.con.close()

    def insertar_seccion(self, sec):
        """Inserta una sección en la tabla secciones."""
        if not self.con:
            raise ConnectionError("Conexión no establecida.")

        sql = '''
        INSERT OR IGNORE INTO secciones (
            sede_id, periodo_academico_id, pnf_id, trayecto_id, tramo_id,
            codigo_seccion, docente_titular_id, docente_auxiliar_id,
            cupo_maximo, cupo_minimo, turno, modalidad,
            aula, horario, dias_semana,
            fecha_inicio, fecha_fin, estado, observaciones
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        '''
        params = (
            sec['sede_id'], sec['periodo_academico_id'],
            sec['pnf_id'], sec['trayecto_id'], sec['tramo_id'],
            sec['codigo_seccion'], sec.get('docente_titular_id'),
            sec.get('docente_auxiliar_id'),
            sec.get('cupo_maximo', 40), sec.get('cupo_minimo', 15),
            sec.get('turno', 'Diurno'), sec.get('modalidad', 'Presencial'),
            sec.get('aula'), sec.get('horario'), sec.get('dias_semana'),
            sec.get('fecha_inicio'), sec.get('fecha_fin'),
            sec.get('estado', 'Planificada'), sec.get('observaciones')
        )

        try:
            cur = self.con.cursor()
            cur.execute(sql, params)
            self.con.commit()
            if cur.rowcount:
                print(f"✅ Sección '{sec['codigo_seccion']}' insertada (ID: {cur.lastrowid}).")
            else:
                print(f"ℹ️  Sección '{sec['codigo_seccion']}' ya existe. Ignorada.")
        except sqlite3.IntegrityError as e:
            print(f"❌ Error de integridad en sección {sec['codigo_seccion']}: {e}")
            self.con.rollback()
        except Exception as e:
            print(f"❌ Error insertando sección {sec['codigo_seccion']}: {e}")
            self.con.rollback()
            raise

    def cargar(self):
        """Carga todas las secciones de secciones_data."""
        if not os.path.exists(self.db_path):
            print(f"Error: base de datos no encontrada en '{self.db_path}'.")
            return

        try:
            self.conectar()
            print("="*50)
            print("Iniciando carga masiva de secciones...")
            print("="*50)
            for sec in self.secciones_data:
                self.insertar_seccion(sec)
            print("\nCarga de secciones finalizada.")
            print("="*50)
        finally:
            self.cerrar()


if __name__ == "__main__":
    cargador = CargadorSecciones(secciones_data)
    cargador.cargar()
