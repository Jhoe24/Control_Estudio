from cargar_pnf_uc import CargadorPNF

pnf_data = {
    'codigo': 'PNF-INF',
    'codigo_nacional': '3147',
    'nombre': 'Programa Nacional de Formación en Informática',
    'nombre_corto': 'PNFI',
    'nivel': 'Técnico Superior Universitario e Ingeniero en Informática',
    'area_conocimiento': 'Informática',
    'duracion_trayectos': 4,  # Solo el número, no texto
    'duracion_semanas': 156,  # Solo el número, no texto
    'total_creditos': 193,    # Solo el número, no texto
    'total_horas': None,
    'modalidad': 'Presencial',
    'titulo_otorga': 'Técnico Superior Universitario en Informática; Ingeniero en Informática',
    'perfil_egreso': 'El egresado del PNFI como Técnico Superior Universitario en Informática es un profesional con formación integral para resolver problemas técnico-informáticos con criterio ético y solidario. Se desempeña con idoneidad en la aplicación de metodologías de trabajo colaborativo, con responsabilidad y ética profesional. El egresado del PNFI como Ingeniero en Informática es un profesional con formación integral para analizar, diseñar, desarrollar e implementar sistemas informáticos complejos de alta calidad. Se desempeña con idoneidad en la conceptualización y ejecución de proyectos informáticos, con responsabilidad y ética profesional.',
    'campo_ocupacional': None,
    'resolucion_creacion': 'Resolución Nº 3147 (2008)',
    'fecha_resolucion': '2008-10-07',  # Formato YYYY-MM-DD
    'version_pensum': '2008 (actualizada diciembre 2011)',
    'coordinador_nacional': 'Humberto González',
    'trayectos': [
        {
            'numero': 0,  # Si es "Inicial", pon 0 o 1 según tu modelo
            'nombre': 'Trayecto Inicial',
            'tipo': None,
            'duracion_semanas': 12,
            'duracion_horas': None,
            'creditos_minimos': 10,
            'creditos_maximos': 10,
            'numero_tramos': 1,
            'objetivos': 'Este trayecto tiene como propósito que el participante se inserte en el PNFI...',
            'competencias': None,
            'perfil_egreso': None,
            'tramos': [],
            'unidades_curriculares': [
                {
                    'codigo': 'MAC015',
                    'nombre': 'Matemática',
                    'nombre_corto': 'Matemática',
                    'area': None,
                    'subarea': None,
                    'eje_formativo': None,
                    'horas_teoricas': None,
                    'horas_practicas': None,
                    'horas_laboratorio': None,
                    'horas_trabajo_independiente': None,
                    'horas_totales': None,
                    'unidades_credito': 5,
                    'tipo': 'Curso',
                    'caracter': None,
                    'modalidad': None,
                    'complejidad': None,
                    'prelaciones': None,
                    'competencias_genericas': None,
                    'competencias_especificas': None,
                    'saberes_cognitivos': None,
                    'saberes_procedimentales': None,
                    'saberes_actitudinales': None,
                    'estrategias_ensenanza': None,
                    'recursos_didacticos': None,
                    'evaluacion': None,
                    'bibliografia': None,
                    'homologacion_clave': None,
                    'clave_especial': None,
                    'tramo_numero': None
                },
                # ...más UCs...
            ]
        },
        # ...más trayectos...
    ]
}

if __name__ == "__main__":
    cargador = CargadorPNF(pnf_data)
    cargador.cargar()