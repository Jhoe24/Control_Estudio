import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from scripts.cargar_pnf_uc import CargadorPNF

from pnf import pnf_data
from trayectos import trayectos_data
from tramos import tramos_data

# Importar todas las UCs por trayecto y tramo
from unidades_curriculares.Trayecto_0.tramo_1 import unidades_tray0_tramo1

from unidades_curriculares.Trayecto_1.tramo_1 import unidades_tray1_tramo1
from unidades_curriculares.Trayecto_1.tramo_2 import unidades_tray1_tramo2
from unidades_curriculares.Trayecto_1.tramo_3 import unidades_tray1_tramo3

from unidades_curriculares.Trayecto_2.tramo_1 import unidades_tray2_tramo1
from unidades_curriculares.Trayecto_2.tramo_2 import unidades_tray2_tramo2
from unidades_curriculares.Trayecto_2.tramo_3 import unidades_tray2_tramo3

from unidades_curriculares.Trayecto_3.tramo_1 import unidades_tray3_tramo1
from unidades_curriculares.Trayecto_3.tramo_2 import unidades_tray3_tramo2
from unidades_curriculares.Trayecto_3.tramo_3 import unidades_tray3_tramo3

from unidades_curriculares.Trayecto_4.tramo_1 import unidades_tray4_tramo1
from unidades_curriculares.Trayecto_4.tramo_2 import unidades_tray4_tramo2
from unidades_curriculares.Trayecto_4.tramo_3 import unidades_tray4_tramo3

# Asignar UCs a cada trayecto (puedes ajustar los índices según corresponda)
trayectos_data[0]['unidades_curriculares'] = unidades_tray0_tramo1

trayectos_data[1]['unidades_curriculares'] = (
    unidades_tray1_tramo1 +
    unidades_tray1_tramo2 +
    unidades_tray1_tramo3
)

trayectos_data[2]['unidades_curriculares'] = (
    unidades_tray2_tramo1 +
    unidades_tray2_tramo2 +
    unidades_tray2_tramo3
)

trayectos_data[3]['unidades_curriculares'] = (
    unidades_tray3_tramo1 +
    unidades_tray3_tramo2 +
    unidades_tray3_tramo3
)

trayectos_data[4]['unidades_curriculares'] = (
    unidades_tray4_tramo1 +
    unidades_tray4_tramo2 +
    unidades_tray4_tramo3
)

# Si necesitas asignar tramos a cada trayecto, puedes hacerlo así:
for trayecto in trayectos_data:
    trayecto['tramos'] = [
        tramo for tramo in tramos_data if tramo['trayecto_numero'] == trayecto['numero']
    ]

# Unir todo en el pnf_data
pnf_data['trayectos'] = trayectos_data

if __name__ == "__main__":
    cargador = CargadorPNF(pnf_data)
    cargador.cargar()