import sqlite3
import os

class CargadorPNF:
    def __init__(self, pnf_data, db_path=None):
        self.pnf_data = pnf_data
        self.db_path = db_path or os.path.join('db', 'sistema_academico.db')
        self.con = sqlite3.connect(self.db_path)

    def insertar_pnf(self):
        cursor = self.con.cursor()
        pnf = self.pnf_data
        cursor.execute('''
            INSERT OR IGNORE INTO pnf (
                codigo, codigo_nacional, nombre, nombre_corto, nivel, area_conocimiento,
                duracion_trayectos, duracion_semanas, total_creditos, total_horas, modalidad,
                titulo_otorga, perfil_egreso, campo_ocupacional, resolucion_creacion, fecha_resolucion,
                version_pensum, coordinador_nacional
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pnf['codigo'], pnf['codigo_nacional'], pnf['nombre'], pnf['nombre_corto'], pnf['nivel'],
            pnf['area_conocimiento'], pnf['duracion_trayectos'], pnf['duracion_semanas'],
            pnf['total_creditos'], pnf['total_horas'], pnf['modalidad'], pnf['titulo_otorga'],
            pnf['perfil_egreso'], pnf['campo_ocupacional'], pnf['resolucion_creacion'],
            pnf['fecha_resolucion'], pnf['version_pensum'], pnf['coordinador_nacional']
        ))
        self.con.commit()
        cursor.execute('SELECT id FROM pnf WHERE codigo = ?', (pnf['codigo'],))
        return cursor.fetchone()[0]

    def insertar_trayecto(self, trayecto, pnf_id):
        cursor = self.con.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO trayectos (
                pnf_id, numero, nombre, tipo, duracion_semanas, duracion_horas, creditos_minimos,
                creditos_maximos, numero_tramos, objetivos, competencias, perfil_egreso
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pnf_id, trayecto['numero'], trayecto['nombre'], trayecto['tipo'], trayecto['duracion_semanas'],
            trayecto['duracion_horas'], trayecto['creditos_minimos'], trayecto['creditos_maximos'],
            trayecto['numero_tramos'], trayecto['objetivos'], trayecto['competencias'], trayecto['perfil_egreso']
        ))
        self.con.commit()
        cursor.execute('SELECT id FROM trayectos WHERE pnf_id = ? AND numero = ?', (pnf_id, trayecto['numero']))
        return cursor.fetchone()[0]

    def insertar_tramo(self, tramo, trayecto_id):
        cursor = self.con.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO tramos (
                trayecto_id, numero, nombre, duracion_semanas, duracion_horas, creditos, objetivos, competencias, estado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trayecto_id, tramo['numero'], tramo['nombre'], tramo['duracion_semanas'], tramo['duracion_horas'],
            tramo['creditos'], tramo.get('objetivos', ''), tramo.get('competencias', ''), tramo.get('estado', 'activo')
        ))
        self.con.commit()
        cursor.execute('SELECT id FROM tramos WHERE trayecto_id = ? AND numero = ?', (trayecto_id, tramo['numero']))
        return cursor.fetchone()[0]

    def insertar_uc(self, uc, pnf_id, trayecto_id, tramo_id=None):
        cursor = self.con.cursor()
        cursor.execute('''
            INSERT INTO unidades_curriculares (
                codigo, nombre, nombre_corto, pnf_id, trayecto_id, tramo_id, area, subarea, eje_formativo,
                horas_teoricas, horas_practicas, horas_laboratorio, horas_trabajo_independiente, horas_totales,
                unidades_credito, tipo, caracter, modalidad, complejidad, prelaciones,
                competencias_genericas, competencias_especificas, saberes_cognitivos, saberes_procedimentales,
                saberes_actitudinales, estrategias_ensenanza, recursos_didacticos, evaluacion, bibliografia,
                homologacion_clave, clave_especial
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            uc['codigo'], uc['nombre'], uc['nombre_corto'], pnf_id, trayecto_id, tramo_id, uc.get('area', None), uc['subarea'],
            uc['eje_formativo'], uc['horas_teoricas'], uc['horas_practicas'], uc['horas_laboratorio'],
            uc['horas_trabajo_independiente'], uc['horas_totales'], uc['unidades_credito'], uc['tipo'],
            uc['caracter'], uc['modalidad'], uc['complejidad'], uc['prelaciones'], uc['competencias_genericas'],
            uc['competencias_especificas'], uc['saberes_cognitivos'], uc['saberes_procedimentales'],
            uc['saberes_actitudinales'], uc['estrategias_ensenanza'], uc['recursos_didacticos'],
            uc['evaluacion'], uc['bibliografia'], uc['homologacion_clave'], uc['clave_especial']
        ))
        self.con.commit()

    def cargar(self):
        print(f"Insertando PNF: {self.pnf_data['nombre']}")
        pnf_id = self.insertar_pnf()
        for trayecto in self.pnf_data.get('trayectos', []):
            print(f"  Insertando Trayecto: {trayecto['nombre']}")
            trayecto_id = self.insertar_trayecto(trayecto, pnf_id)
            # Tramos (opcional)
            tramos = trayecto.get('tramos', [])
            tramos_ids = {}
            for tramo in tramos:
                print(f"    Insertando Tramo: {tramo['nombre']}")
                tramo_id = self.insertar_tramo(tramo, trayecto_id)
                tramos_ids[tramo['numero']] = tramo_id
            # UCs
            for uc in trayecto.get('unidades_curriculares', []):
                tramo_id = None
                if 'tramo_numero' in uc and uc['tramo_numero'] in tramos_ids:
                    tramo_id = tramos_ids[uc['tramo_numero']]
                print(f"    Insertando UC: {uc['nombre']}")
                self.insertar_uc(uc, pnf_id, trayecto_id, tramo_id)
        self.con.close()
        print("\nCarga masiva finalizada.")
