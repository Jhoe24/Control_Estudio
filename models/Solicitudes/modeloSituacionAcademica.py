import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
import webbrowser
import locale 

# Intenta establecer el idioma local para el formato de fecha (día y mes en español)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        pass


class ModeloSituacionAcademica:
    def __init__(self, datosEstudiante, listNotas):
        self.datosEstudiante = datosEstudiante
        self.listNotas = listNotas
        self._fuente = "Helvetica"

        # --- Configuración de rutas y nombres de archivo ---
        documents_path = Path.home() / "Documents"
        if not documents_path.exists():
            documents_path = Path.home() / "Documentos"

        pdf_output_dir = documents_path / "Situaciones Academicas"
        pdf_output_dir.mkdir(parents=True, exist_ok=True)
        
        cedula = datosEstudiante.get('documento_identidad', 'SIN_CEDULA')
        self._nombreArchivo = f"Situacion_Academica_{cedula}_{datetime.now().strftime('%Y%m%d')}_V2.pdf" # V2 para el diseño final
        self.filepath = pdf_output_dir / self._nombreArchivo

        # --- Contenido del documento ---
        self._imgLogo = "resources/images/logo4.jpg" 

        nucleo = datosEstudiante.get('sede_nombre', 'N/A')
        self._cabeceraIzquierda = {
            "texto": f"""<font size='8' face='Helvetica-Bold'>REPÚBLICA BOLIVARIANA DE VENEZUELA</font><br/>
                         <font size='8' face='Helvetica-Bold'>UNIVERSIDAD POLITÉCNICA TERRITORIAL</font><br/>
                         <font size='8' face='Helvetica-Bold'>DEL ESTADO BARINAS</font><br/>
                         <font size='8' face='Helvetica-Bold'>"JOSÉ FÉLIX RIBAS"</font><br/>
                         <font size='7'>R.I.F.: G-20009502-4</font>""",
            "tamanoFuente": 10
        }
        
        self._cabeceraDerecha = {
            "texto": f"""<font face='Helvetica-Bold'>SECRETARÍA GENERAL</font><br/>
                          Coordinación de Admisión, Seguimiento, Registro y Control de Estudio<br/>
                          Núcleo {nucleo}""",
            "tamanoFuente": 10
        }
        
        self._titulo = {"texto": "SITUACION ACADEMICA", "tamanoFuente": 14}
        
        # TABLA DE DATOS DEL ESTUDIANTE
        cedula_completa = f"{datosEstudiante.get('tipo_documento', 'V')}-{cedula}"
        self._datosPrimeraTabla = [
            [
                f"Documento de Identidad: <b>{cedula_completa}</b>",
                "Apellidos y Nombres:",
                f"<b>{datosEstudiante.get('apellidos', '').upper()}, {datosEstudiante.get('nombres', '').upper()}</b>"
            ],
            [
                f"Cursando P.N.F. en: <b>{datosEstudiante.get('pnf_nombre', 'N/A').upper()}</b>",
                "Índice Académico Acumulado:",
                f"<b>{str(datosEstudiante.get('indiceAcademico', 'N/A'))}</b>"
            ]
        ]
        
        self._cabecera_tabla_notas = ["Año", "Trayecto", "Unidad Curricular Cursada", "Nota", "Asist.", "U.C.", "Condición"]

        # Fecha dinámica
        now = datetime.now()
        fecha_str_upper = now.strftime('%A %d DE %B DE %Y, %I:%M:%S %p').upper()
        self._fecha_encabezado = fecha_str_upper.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')


        # Firma (usada en página 1 y 2)
        self._firmaCoordinador = {
            "texto": f"""<br/>Lcdo. Henry Rujano Herrera<br/>
                          V-14.002.390<br/>
                          Coordinador de Admisión, Seguimiento, Registro y Control de Estudio Núcleo {nucleo}""",
            "tamanoFuente": 9
        }

        # ************ Título del Pie de Página más grande ************
        self._tituloPiePagina = "<b><font size='10'>Tecnología al Servicio de la Comunidad</font></b>"
        
        # Pie de página con etiquetas de fuente anidadas
        self.tablaPiepagina = [
            "<font size='8'><b>Extensión Barinas</b><br/><font size='7'>Av. Industrial Frente al Aserradero El Pozón<br/>(0273)5413579 - (0273)5413657</font></font>",
            "<font size='8'><b>Núcleo Barinitas</b><br/><font size='7'>Av. Principal, Sector El Cacao<br/>(0278)2215001</font></font>",
            "<font size='8'><b>Núcleo Socopó</b><br/><font size='7'>Carrera 7 Vía El Uno<br/>(0273)8718535</font></font>",
            "<font size='8'><b>Extensión Pedraza</b><br/><font size='7'>Hacienda Ticoporo, Ciudad Bolivia<br/>(0273)9210269</font></font>"
        ]
    
    # Nuevo método para la cabecera de la Página 2+ (más compacta)
    def _cabecera_paginas_secundarias(self, canvas, doc):
        canvas.saveState()
        styles = getSampleStyleSheet()
        style_header = ParagraphStyle(name='header_style', parent=styles['Normal'], alignment=TA_CENTER, fontName=self._fuente, fontSize=8)
        style_right_date = ParagraphStyle(name='right_date', parent=styles['Normal'], alignment=TA_RIGHT, fontName=self._fuente, fontSize=8)
        
        logo_img = None
        if os.path.exists(self._imgLogo):
            logo_img = Image(self._imgLogo, 0.7*inch, 0.7*inch)
            logo_img.hAlign = 'CENTER'

        p_left_header = Paragraph(self._cabeceraIzquierda['texto'], style_header)
        p_right_header = Paragraph(self._cabeceraDerecha['texto'], style_header)
        
        # Tabla de cabecera: Mismo layout que página 1
        header_table = Table([[logo_img, p_left_header, p_right_header]], 
                             colWidths=[1*inch, 3*inch, 3*inch])
        header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        
        w, h = header_table.wrapOn(canvas, doc.width, doc.topMargin)
        header_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h + 0.5*cm) 

        # Línea de Fecha y Página
        p_fecha = Paragraph(self._fecha_encabezado, style_right_date)
        p_pagina = Paragraph(f"Pag: {doc.page}", style_right_date) 
        
        fecha_page_table = Table([["", p_fecha, p_pagina]], colWidths=[1*inch, 5.5*inch, 0.5*inch])
        fecha_page_table.setStyle(TableStyle([('ALIGN', (1, 0), (2, 0), 'RIGHT')]))
        
        w, h_fp = fecha_page_table.wrapOn(canvas, doc.width, doc.topMargin)
        fecha_page_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        
        # Firma centrada debajo de la cabecera (como en image_3adbbe.png)
        style_firma_secundaria = ParagraphStyle(name='Firma_Secundaria', parent=styles['Normal'], fontName=self._fuente, fontSize=self._firmaCoordinador['tamanoFuente'], alignment=TA_CENTER, leading=11, spaceBefore=10)
        p_firma = Paragraph(self._firmaCoordinador['texto'].replace("<br/>", ""), style_firma_secundaria)

        # Ajustamos la posición de la firma de la página 2
        p_firma.wrapOn(canvas, doc.width, 10)
        p_firma.drawOn(canvas, doc.leftMargin + (doc.width - p_firma.minWidth()) / 2, doc.height + doc.topMargin - h - 0.5*cm)


        canvas.restoreState()


    def _cabecera_pie_pagina(self, canvas, doc):
        """ Dibuja la cabecera (Página 1) y el pie de página (Página 1). """
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        # Estilos
        style_header = ParagraphStyle(name='header_style', parent=styles['Normal'], alignment=TA_CENTER, fontName=self._fuente, fontSize=8)
        style_right_date = ParagraphStyle(name='right_date', parent=styles['Normal'], alignment=TA_RIGHT, fontName=self._fuente, fontSize=8)
        
        # --- Cabecera: Logo y Texto UPTJFR ---
        logo_img = None
        if os.path.exists(self._imgLogo):
            logo_img = Image(self._imgLogo, 0.7*inch, 0.7*inch)
            logo_img.hAlign = 'CENTER'

        p_left_header = Paragraph(self._cabeceraIzquierda['texto'], style_header)
        p_right_header = Paragraph(self._cabeceraDerecha['texto'], style_header)
        
        # Cabecera de la tabla. Ajustamos los colWidths para alinear mejor
        header_table = Table([[logo_img, p_left_header, p_right_header]], 
                             colWidths=[1*inch, 3*inch, 3*inch])
        header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        
        w, h = header_table.wrapOn(canvas, doc.width, doc.topMargin)
        # Dibujar la cabecera en la parte superior. (Mismo ajuste que en la página 2)
        header_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h + 0.5*cm) 

        # --- Línea de Fecha y Página ---
        p_fecha = Paragraph(self._fecha_encabezado, style_right_date)
        p_pagina = Paragraph(f"Pag: {doc.page}", style_right_date) 
        
        fecha_page_table = Table([["", p_fecha, p_pagina]], colWidths=[1*inch, 5.5*inch, 0.5*inch])
        fecha_page_table.setStyle(TableStyle([('ALIGN', (1, 0), (2, 0), 'RIGHT')]))
        
        w, h_fp = fecha_page_table.wrapOn(canvas, doc.width, doc.topMargin)
        fecha_page_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        
        # --- Pie de Página (Solo en Página 1) ---
        styles_normal = getSampleStyleSheet()['Normal']
        style_center = ParagraphStyle(name='center_footer', parent=styles_normal, alignment=TA_CENTER, fontSize=8, fontName=self._fuente)
        
        # Título del pie de página (ajustado en size='10' en el init)
        p_titulo_footer = Paragraph(self._tituloPiePagina, styles_normal)
        w, h_tf = p_titulo_footer.wrap(doc.width, doc.bottomMargin)
        
        # Dibujar el título centrado
        p_titulo_footer.drawOn(canvas, doc.leftMargin + (doc.width - w) / 2, h_tf + 0.8*inch)

        # La tabla del pie de página (CORREGIDA a 1x4)
        data_footer = [
            [Paragraph(cell, styles_normal) for cell in self.tablaPiepagina]
        ]
        # ColWidths: doc.width/4.0 es para que se divida en 4 columnas iguales.
        footer_table = Table(data_footer, colWidths=[doc.width/4.0] * 4) 
        footer_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                          ('LINEABOVE', (0,0), (-1,0), 0.5, colors.black) # Línea divisoria, como en la imagen
                                         ]))
        w, h_ft = footer_table.wrap(doc.width, doc.bottomMargin)
        footer_table.drawOn(canvas, doc.leftMargin, 0.3*inch)

        canvas.restoreState()

    def generar_pdf(self):
        """Genera el archivo PDF con los datos personales sin bordes,
        cabecera solo en la primera página y pie final único."""
        doc = SimpleDocTemplate(
            str(self.filepath),
            pagesize=letter,
            topMargin=4.5 * cm,
            bottomMargin=2 * cm,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm
        )

        Story = []
        styles = getSampleStyleSheet()

        # --- Estilos ---
        style_titulo = ParagraphStyle(
            name='Titulo',
            parent=styles['h1'],
            fontName='Helvetica-Bold',
            fontSize=self._titulo['tamanoFuente'],
            alignment=TA_CENTER,
            spaceAfter=10
        )
        style_info_label = ParagraphStyle(
            name='InfoLabel',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            alignment=TA_LEFT
        )
        style_info_value = ParagraphStyle(
            name='InfoValue',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            alignment=TA_LEFT
        )
        style_firma = ParagraphStyle(
            name='Firma',
            parent=styles['Normal'],
            fontName=self._fuente,
            fontSize=self._firmaCoordinador['tamanoFuente'],
            alignment=TA_CENTER,
            leading=11,
            spaceBefore=30,
            spaceAfter=25
        )
        style_center = ParagraphStyle(
            name='center_footer',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            fontSize=8,
            fontName=self._fuente
        )

        # --- Título ---
        Story.append(Paragraph(self._titulo['texto'], style_titulo))
        Story.append(Spacer(1, 0.2 * inch))

        # --- Datos personales del estudiante (sin bordes, tipo texto) ---
        cedula = f"{self.datosEstudiante.get('tipo_documento', 'V')}-{self.datosEstudiante.get('documento_identidad', 'N/A')}"
        nombre_completo = f"{self.datosEstudiante.get('apellidos', '').upper()}, {self.datosEstudiante.get('nombres', '').upper()}"
        pnf = self.datosEstudiante.get('pnf_nombre', 'N/A').upper()
        indice = str(self.datosEstudiante.get('indiceAcademico', 'N/A'))

        datos_layout = [
            [Paragraph(f"<b>Documento de Identidad:</b> {cedula}", style_info_value),
            Paragraph(f"<b>Apellidos y Nombres:</b> {nombre_completo}", style_info_value)],
            [Paragraph(f"<b>Cursando P.N.F. en:</b> {pnf}", style_info_value),
            Paragraph(f"<b>Índice Académico Acumulado:</b> {indice}", style_info_value)]
        ]

        tabla_datos = Table(datos_layout, colWidths=[3.2 * inch, 3.2 * inch])
        tabla_datos.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            # Sin bordes, totalmente limpio
            ('BOX', (0, 0), (-1, -1), 0, colors.white),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ]))
        Story.append(tabla_datos)
        Story.append(Spacer(1, 0.25 * inch))

        # --- Tabla de notas ---
        data_notas = [self._cabecera_tabla_notas]
        for nota in self.listNotas:
            valor_nota = nota.get('nota', 0.0)
            condicion = "APROBADA" if valor_nota >= 10 else "REPROBADA"
            trayecto_split = nota.get('nombre_trayecto', 'N/A').split(' ')
            trayecto_val = trayecto_split[-1] if trayecto_split[-1] != 'Inicial' else 'Inicial'

            data_notas.append([
                nota.get('periodo_academico', 'N/A').split('-')[0],
                trayecto_val,
                Paragraph(nota.get('nombre_unidad_curricular', 'N/A'), style_info_value),
                f"{valor_nota:.2f}",
                str(nota.get('asistencia', 'N/A')),
                str(nota.get('unidades_credito', 'N/A')),
                condicion
            ])

        col_widths = [0.6 * inch, 0.8 * inch, 3.5 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 1.0 * inch]
        tabla_notas = Table(data_notas, colWidths=col_widths)
        tabla_notas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), self._fuente),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ]))
        Story.append(tabla_notas)
        Story.append(Spacer(1, 0.3 * inch))

        # --- Firma ---
        Story.append(Paragraph(
            "____________________________<br/>" + self._firmaCoordinador["texto"],
            style_firma
        ))

        # --- Pie de página (solo al final) ---
        Story.append(Paragraph(self._tituloPiePagina, style_center))
        Story.append(Spacer(1, 0.2 * inch))

        data_footer = [[Paragraph(cell, style_center) for cell in self.tablaPiepagina]]
        footer_table = Table(data_footer, colWidths=[doc.width / 4.0] * 4)
        footer_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black)
        ]))
        Story.append(footer_table)

        # --- Construcción ---
        # --- Construcción ---
        try:
            from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
        except Exception:
            print("Falta reportlab.platypus.BaseDocTemplate/PageTemplate/Frame")
            return None

        try:
            # --- Documento base ---
            doc = BaseDocTemplate(
                str(self.filepath),
                pagesize=letter,
                leftMargin=1.5 * cm,
                rightMargin=1.5 * cm,
                topMargin=4.5 * cm,   # margen pensado para la primera página
                bottomMargin=2 * cm
            )

            # --- Calculamos espacio extra para las páginas restantes (para eliminar hueco) ---
            small_top = 1.0 * cm                     # margen superior que queremos en páginas 2+
            extra = doc.topMargin - small_top        # cuánto "recuperamos" para las páginas siguientes

            # Frame para la primera página (respetando el margen grande)
            frame_primera = Frame(doc.leftMargin,
                                doc.bottomMargin,
                                doc.width,
                                doc.height,
                                id='frame_primera')

            # Frame para las páginas restantes (aumentamos la altura para ocupar el espacio del membrete)
            frame_restantes = Frame(doc.leftMargin,
                                    doc.bottomMargin,
                                    doc.width,
                                    doc.height + extra,
                                    id='frame_restantes')

            # --- Función que dibuja el membrete (solo 1ª página) ---
            def _solo_cabecera(canvas, _doc):
                canvas.saveState()
                styles = getSampleStyleSheet()
                style_header = ParagraphStyle(
                    name='header_style',
                    parent=styles['Normal'],
                    alignment=TA_CENTER,
                    fontName=self._fuente,
                    fontSize=8
                )
                style_right_date = ParagraphStyle(
                    name='right_date',
                    parent=styles['Normal'],
                    alignment=TA_RIGHT,
                    fontName=self._fuente,
                    fontSize=8
                )

                # Logo (si existe)
                logo_img = None
                if os.path.exists(self._imgLogo):
                    logo_img = Image(self._imgLogo, 0.7 * inch, 0.7 * inch)
                    logo_img.hAlign = 'CENTER'

                p_left_header = Paragraph(self._cabeceraIzquierda['texto'], style_header)
                p_right_header = Paragraph(self._cabeceraDerecha['texto'], style_header)

                header_table = Table([[logo_img, p_left_header, p_right_header]],
                                    colWidths=[1 * inch, 3 * inch, 3 * inch])
                header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))

                # Dibujamos en la parte superior (calculamos Y usando page height)
                page_w, page_h = doc.pagesize
                w, h = header_table.wrap(page_w - doc.leftMargin - doc.rightMargin, doc.topMargin)
                header_y = page_h - (0.75 * cm) - h   # ajuste fino, puedes modificar 0.75*cm si requiere
                header_table.drawOn(canvas, doc.leftMargin, header_y)

                # Fecha y número de página a la derecha
                p_fecha = Paragraph(self._fecha_encabezado, style_right_date)
                p_pagina = Paragraph(f"Pag: {_doc.page}", style_right_date)
                fecha_page_table = Table([["", p_fecha, p_pagina]], colWidths=[1 * inch, 5.5 * inch, 0.5 * inch])
                fecha_page_table.setStyle(TableStyle([('ALIGN', (1, 0), (2, 0), 'RIGHT')]))
                w_fp, h_fp = fecha_page_table.wrap(page_w - doc.leftMargin - doc.rightMargin, doc.topMargin)
                fecha_page_table.drawOn(canvas, doc.leftMargin, header_y - 0.2 * cm - h_fp)

                # Indicar que a partir de la siguiente página use la plantilla 'PaginasRestantes'
                try:
                    _doc.handle_nextPageTemplate('PaginasRestantes')
                except Exception:
                    # fallback: establecer atributo interno (algunos entornos antiguos)
                    setattr(_doc, '_nextPageTemplate', 'PaginasRestantes')

                canvas.restoreState()

            # --- Función para páginas siguientes: sólo número de página (sin membrete) ---
            def _sin_cabecera(canvas, _doc):
                canvas.saveState()
                style_right_date = ParagraphStyle(
                    name='right_date_small',
                    parent=getSampleStyleSheet()['Normal'],
                    alignment=TA_RIGHT,
                    fontName=self._fuente,
                    fontSize=8
                )
                p_pagina = Paragraph(f"Pag: {_doc.page}", style_right_date)
                page_w, page_h = doc.pagesize
                w_p, h_p = p_pagina.wrap(doc.width, doc.topMargin)
                # colocarlo cerca del borde superior (con margen reducido)
                p_pagina.drawOn(canvas, doc.leftMargin, page_h - 0.9 * cm - h_p)
                canvas.restoreState()

            # --- Plantillas de página ---
            template_primera = PageTemplate(id='PrimeraPagina', frames=[frame_primera], onPage=_solo_cabecera)
            template_restantes = PageTemplate(id='PaginasRestantes', frames=[frame_restantes], onPage=_sin_cabecera)
            doc.addPageTemplates([template_primera, template_restantes])

            # --- Construcción del Story (todo inline, sin funciones auxiliares externas) ---
            Story = []
            styles = getSampleStyleSheet()

            # Estilos principales
            style_titulo = ParagraphStyle(name='Titulo', parent=styles['h1'], fontName='Helvetica-Bold',
                                        fontSize=self._titulo['tamanoFuente'], alignment=TA_CENTER, spaceAfter=8)
            style_info_value = ParagraphStyle(name='InfoValue', parent=styles['Normal'], fontName=self._fuente,
                                            fontSize=9, leading=12, alignment=TA_LEFT)
            style_firma = ParagraphStyle(name='Firma', parent=styles['Normal'], fontName=self._fuente,
                                        fontSize=self._firmaCoordinador['tamanoFuente'], alignment=TA_CENTER,
                                        leading=11, spaceBefore=28, spaceAfter=10)
            style_center = ParagraphStyle(name='center_footer', parent=styles['Normal'], alignment=TA_CENTER,
                                        fontSize=8, fontName=self._fuente)

            # Título
            Story.append(Paragraph(self._titulo['texto'], style_titulo))
            Story.append(Spacer(1, 0.15 * inch))

            # Datos personales (sin bordes, igual al modelo)
            cedula = f"{self.datosEstudiante.get('tipo_documento', 'V')}-{self.datosEstudiante.get('documento_identidad', 'N/A')}"
            nombre_completo = f"{self.datosEstudiante.get('apellidos', '').upper()}, {self.datosEstudiante.get('nombres', '').upper()}"
            pnf = self.datosEstudiante.get('pnf_nombre', 'N/A').upper()
            indice = str(self.datosEstudiante.get('indiceAcademico', 'N/A'))

            datos_layout = [
                [Paragraph(f"<b>Documento de Identidad:</b> {cedula}", style_info_value),
                Paragraph(f"<b>Apellidos y Nombres:</b> {nombre_completo}", style_info_value)],
                [Paragraph(f"<b>Cursando P.N.F. en:</b> {pnf}", style_info_value),
                Paragraph(f"<b>Índice Académico Acumulado:</b> {indice}", style_info_value)]
            ]
            tabla_datos = Table(datos_layout, colWidths=[doc.width * 0.48, doc.width * 0.48])
            tabla_datos.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOX', (0, 0), (-1, -1), 0, colors.white),
                ('GRID', (0, 0), (-1, -1), 0, colors.white),
            ]))
            Story.append(tabla_datos)
            Story.append(Spacer(1, 0.18 * inch))

            # Tabla de notas
            data_notas = [self._cabecera_tabla_notas]
            for nota in self.listNotas:
                valor_nota = nota.get('nota', 0.0)
                condicion = "APROBADA" if valor_nota >= 12 else "REPROBADA"
                trayecto_split = nota.get('nombre_trayecto', 'N/A').split(' ')
                trayecto_val = trayecto_split[-1] if trayecto_split[-1] != 'Inicial' else 'Inicial'
                data_notas.append([
                    nota.get('periodo_academico', 'N/A').split('-')[0],
                    trayecto_val,
                    Paragraph(nota.get('nombre_unidad_curricular', 'N/A'), style_info_value),
                    f"{valor_nota:.2f}",
                    str(nota.get('asistencia', 'N/A')),
                    str(nota.get('unidades_credito', 'N/A')),
                    condicion
                ])

            col_widths = [0.6 * inch, 0.8 * inch, 3.5 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 1.0 * inch]
            tabla_notas = Table(data_notas, colWidths=col_widths)
            tabla_notas.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, -1), self._fuente),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
            ]))
            Story.append(tabla_notas)
            Story.append(Spacer(1, 0.18 * inch))

            # Firma
            Story.append(Paragraph("____________________________<br/>" + self._firmaCoordinador["texto"], style_firma))

            # Pie (solo al final)
            Story.append(Spacer(1, 0.08 * inch))
            Story.append(Paragraph(self._tituloPiePagina, style_center))
            Story.append(Spacer(1, 0.12 * inch))
            data_footer = [[Paragraph(cell, style_center) for cell in self.tablaPiepagina]]
            footer_table = Table(data_footer, colWidths=[doc.width / 4.0] * 4)
            footer_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black)
            ]))
            Story.append(footer_table)

            # --- Construir PDF ---
            doc.build(Story)
            return str(self.filepath)

        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            return None

    

# if __name__ == '__main__':
#     print("Iniciando prueba de generación de Situación Académica (Diseño Final)...")

#     # 1. Datos de ejemplo para el estudiante
#     sample_datos_estudiante = {
#         'documento_identidad': '10999894',
#         'tipo_documento': 'V',
#         'nombres': 'Rafael Gabriel',
#         'apellidos': 'Semejal Herrera',
#         'pnf_nombre': 'Medicina Veterinaria',
#         'sede_nombre': 'Socopó',
#         'indiceAcademico': '17.546392'
#     }

#     # 2. Lista de ejemplo de notas (LO SUFICIENTEMENTE LARGA PARA FORZAR 2 PÁGINAS)
#     sample_lista_notas = [
#         {'periodo_academico': '2017-I', 'nombre_trayecto': 'Inicial', 'nombre_unidad_curricular': 'INTRODUCCION A LA MEDICINA VETERINARIA', 'nota': 16.00, 'asistencia': 90, 'unidades_credito': 2},
#         {'periodo_academico': '2017-I', 'nombre_trayecto': 'Inicial', 'nombre_unidad_curricular': 'LECTURA Y COMPRENSION', 'nota': 19.00, 'asistencia': 100, 'unidades_credito': 1},
#         {'periodo_academico': '2017-I', 'nombre_trayecto': 'Inicial', 'nombre_unidad_curricular': 'APLICACIÓN DE LAS TICS', 'nota': 19.00, 'asistencia': 98, 'unidades_credito': 1},
#         {'periodo_academico': '2017-I', 'nombre_trayecto': 'Inicial', 'nombre_unidad_curricular': 'MATEMATICA', 'nota': 18.00, 'asistencia': 90, 'unidades_credito': 3},
#         {'periodo_academico': '2017-I', 'nombre_trayecto': 'Inicial', 'nombre_unidad_curricular': 'PROYECTO NACIONAL Y NUEVA CIUDADANIA', 'nota': 19.00, 'asistencia': 92, 'unidades_credito': 3},
#         {'periodo_academico': '2017-I', 'nombre_trayecto': 'Inicial', 'nombre_unidad_curricular': 'TALLER DE INTRODUCCION A LA UNIVERSIDAD Y AL P.N.F.', 'nota': 19.00, 'asistencia': 85, 'unidades_credito': 2},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'ALIMENTACION Y NUTRICION', 'nota': 20.00, 'asistencia': 100, 'unidades_credito': 8},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'BIOQUIMICA', 'nota': 15.00, 'asistencia': 100, 'unidades_credito': 7},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'DEPORTE Y ACTIVIDAD FISICA', 'nota': 19.00, 'asistencia': 95, 'unidades_credito': 1},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'ESTADISTICA Y DISEÑO EXPERIMENTAL', 'nota': 19.00, 'asistencia': 100, 'unidades_credito': 1},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'FISIOLOGIA', 'nota': 18.00, 'asistencia': 100, 'unidades_credito': 7},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'MORFOFISIOLOGIA I', 'nota': 15.00, 'asistencia': 100, 'unidades_credito': 9},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'ORGANIZACION COMUNITARIA Y SU AMBIENTE', 'nota': 19.00, 'asistencia': 100, 'unidades_credito': 4},
#         {'periodo_academico': '2018-I', 'nombre_trayecto': 'Primero', 'nombre_unidad_curricular': 'PROYECTO I: Introducción a la Producción Animal desde la Medicina Veterinaria', 'nota': 18.00, 'asistencia': 90, 'unidades_credito': 8},
#         {'periodo_academico': '2019-I', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'SISTEMAS DE PRODUCCIÓN ANIMAL I', 'nota': 17.00, 'asistencia': 100, 'unidades_credito': 3},
#         {'periodo_academico': '2019-I', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'ELECTIVA', 'nota': 17.00, 'asistencia': 75, 'unidades_credito': 1},
#         {'periodo_academico': '2019-I', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'ÉTICA Y DEONTOLOGÍA VETERINARIA', 'nota': 18.00, 'asistencia': 100, 'unidades_credito': 1},
#         {'periodo_academico': '2019-I', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'GENÉTICA', 'nota': 19.00, 'asistencia': 77, 'unidades_credito': 7},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'MICROBIOLOGÍA', 'nota': 20.00, 'asistencia': 77, 'unidades_credito': 5},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'MORFOFISIOLOGÍA II', 'nota': 15.00, 'asistencia': 77, 'unidades_credito': 9},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'ORIENTACIÓN E INTEGRACIÓN PSICOSOCIAL', 'nota': 19.00, 'asistencia': 77, 'unidades_credito': 2},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'PROYECTO II: Atención al Cuidado y Producción Animal', 'nota': 19.00, 'asistencia': 75, 'unidades_credito': 8},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'RECREACIÓN Y CULTURA', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 1},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'SISTEMAS DE PRODUCCIÓN ANIMAL II', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 9},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'PATOLOGÍA', 'nota': 18.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'FARMACOLOGÍA', 'nota': 15.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'TOXICOLOGÍA', 'nota': 19.00, 'asistencia': 90, 'unidades_credito': 4},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'EPIDEMIOLOGÍA', 'nota': 16.00, 'asistencia': 90, 'unidades_credito': 3},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CLÍNICA DE PEQUEÑOS ANIMALES', 'nota': 17.00, 'asistencia': 95, 'unidades_credito': 8},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CIRUGÍA VETERINARIA', 'nota': 14.00, 'asistencia': 95, 'unidades_credito': 6},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'SALUD PÚBLICA', 'nota': 19.00, 'asistencia': 95, 'unidades_credito': 4},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'ORIENTACIÓN E INTEGRACIÓN PSICOSOCIAL', 'nota': 19.00, 'asistencia': 77, 'unidades_credito': 2},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'PROYECTO II: Atención al Cuidado y Producción Animal', 'nota': 19.00, 'asistencia': 75, 'unidades_credito': 8},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'RECREACIÓN Y CULTURA', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 1},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'SISTEMAS DE PRODUCCIÓN ANIMAL II', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 9},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'PATOLOGÍA', 'nota': 18.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'FARMACOLOGÍA', 'nota': 15.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'TOXICOLOGÍA', 'nota': 19.00, 'asistencia': 90, 'unidades_credito': 4},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'EPIDEMIOLOGÍA', 'nota': 16.00, 'asistencia': 90, 'unidades_credito': 3},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CLÍNICA DE PEQUEÑOS ANIMALES', 'nota': 17.00, 'asistencia': 95, 'unidades_credito': 8},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CIRUGÍA VETERINARIA', 'nota': 14.00, 'asistencia': 95, 'unidades_credito': 6},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'SALUD PÚBLICA', 'nota': 19.00, 'asistencia': 95, 'unidades_credito': 4},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'ORIENTACIÓN E INTEGRACIÓN PSICOSOCIAL', 'nota': 19.00, 'asistencia': 77, 'unidades_credito': 2},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'PROYECTO II: Atención al Cuidado y Producción Animal', 'nota': 19.00, 'asistencia': 75, 'unidades_credito': 8},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'RECREACIÓN Y CULTURA', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 1},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'SISTEMAS DE PRODUCCIÓN ANIMAL II', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 9},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'PATOLOGÍA', 'nota': 18.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'FARMACOLOGÍA', 'nota': 15.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'TOXICOLOGÍA', 'nota': 19.00, 'asistencia': 90, 'unidades_credito': 4},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'EPIDEMIOLOGÍA', 'nota': 16.00, 'asistencia': 90, 'unidades_credito': 3},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CLÍNICA DE PEQUEÑOS ANIMALES', 'nota': 17.00, 'asistencia': 95, 'unidades_credito': 8},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CIRUGÍA VETERINARIA', 'nota': 14.00, 'asistencia': 95, 'unidades_credito': 6},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'SALUD PÚBLICA', 'nota': 19.00, 'asistencia': 95, 'unidades_credito': 4},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'ORIENTACIÓN E INTEGRACIÓN PSICOSOCIAL', 'nota': 19.00, 'asistencia': 77, 'unidades_credito': 2},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'PROYECTO II: Atención al Cuidado y Producción Animal', 'nota': 19.00, 'asistencia': 75, 'unidades_credito': 8},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'RECREACIÓN Y CULTURA', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 1},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'SISTEMAS DE PRODUCCIÓN ANIMAL II', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 9},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'PATOLOGÍA', 'nota': 18.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'FARMACOLOGÍA', 'nota': 15.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'TOXICOLOGÍA', 'nota': 19.00, 'asistencia': 90, 'unidades_credito': 4},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'EPIDEMIOLOGÍA', 'nota': 16.00, 'asistencia': 90, 'unidades_credito': 3},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CLÍNICA DE PEQUEÑOS ANIMALES', 'nota': 17.00, 'asistencia': 95, 'unidades_credito': 8},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CIRUGÍA VETERINARIA', 'nota': 14.00, 'asistencia': 95, 'unidades_credito': 6},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'SALUD PÚBLICA', 'nota': 19.00, 'asistencia': 95, 'unidades_credito': 4},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'ORIENTACIÓN E INTEGRACIÓN PSICOSOCIAL', 'nota': 19.00, 'asistencia': 77, 'unidades_credito': 2},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'PROYECTO II: Atención al Cuidado y Producción Animal', 'nota': 19.00, 'asistencia': 75, 'unidades_credito': 8},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'RECREACIÓN Y CULTURA', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 1},
#         {'periodo_academico': '2019-II', 'nombre_trayecto': 'Segundo', 'nombre_unidad_curricular': 'SISTEMAS DE PRODUCCIÓN ANIMAL II', 'nota': 18.00, 'asistencia': 77, 'unidades_credito': 9},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'PATOLOGÍA', 'nota': 18.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'FARMACOLOGÍA', 'nota': 15.00, 'asistencia': 90, 'unidades_credito': 6},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'TOXICOLOGÍA', 'nota': 19.00, 'asistencia': 90, 'unidades_credito': 4},
#         {'periodo_academico': '2020-I', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'EPIDEMIOLOGÍA', 'nota': 16.00, 'asistencia': 90, 'unidades_credito': 3},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CLÍNICA DE PEQUEÑOS ANIMALES', 'nota': 17.00, 'asistencia': 95, 'unidades_credito': 8},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'CIRUGÍA VETERINARIA', 'nota': 14.00, 'asistencia': 95, 'unidades_credito': 6},
#         {'periodo_academico': '2020-II', 'nombre_trayecto': 'Tercero', 'nombre_unidad_curricular': 'SALUD PÚBLICA', 'nota': 19.00, 'asistencia': 95, 'unidades_credito': 4},
#     ]

#     # 3. Instanciar la clase y generar el PDF
#     reporte_generator = ModeloSituacionAcademica(sample_datos_estudiante, sample_lista_notas)
#     ruta_pdf = reporte_generator.generar_pdf()

#     # 4. Mostrar resultado y abrir el archivo
#     if ruta_pdf:
#         print(f"¡Éxito! PDF generado en: {ruta_pdf}")
#         print("Abriendo el archivo...")
#         webbrowser.open(ruta_pdf)
#     else:
#         print("Error: No se pudo generar el PDF.")