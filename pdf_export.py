from reportlab.lib.pagesizes import A4, landscape, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from database import (
    get_project_by_id,
    get_presupuesto_by_project,
    get_budget_total,
    get_cubicaciones_by_project
)


def format_clp(value):
    try:
        return "$" + f"{float(value):,.0f}".replace(",", ".")
    except Exception:
        return "$0"


def unidad_visible(unidad):
    unidades = {
        "m2": "m²",
        "m3": "m³",
        "kg": "kg",
        "ml": "ml",
        "un": "un"
    }
    return unidades.get(unidad, unidad or "")


def header_footer(canvas, doc):
    canvas.saveState()

    width, height = doc.pagesize

    canvas.setFillColor(colors.HexColor("#0F172A"))
    canvas.rect(0, height - 1.2 * cm, width, 1.2 * cm, fill=True, stroke=False)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(1.5 * cm, height - 0.75 * cm, "CubiChile")

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawRightString(
        width - 1.5 * cm,
        0.8 * cm,
        f"Página {doc.page}"
    )

    canvas.restoreState()


def base_styles():
    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=14
    )

    subtitle = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10
    )

    section = ParagraphStyle(
        "SectionCustom",
        parent=styles["Heading2"],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=8
    )

    normal = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155")
    )

    small = ParagraphStyle(
        "SmallCustom",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#475569")
    )

    return title, subtitle, section, normal, small


def project_table(project):
    project_id, name, client, location, description, created_at = project

    data = [
        ["Proyecto", name or ""],
        ["Cliente", client or "Sin cliente"],
        ["Ubicación", location or "Sin ubicación"],
        ["Fecha creación", created_at or ""],
        ["Descripción", description or "Sin descripción registrada."]
    ]

    table = Table(data, colWidths=[4 * cm, 13 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F8FAFC")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#0F172A")),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    return table


def export_presupuesto_pdf(project_id, filepath):
    project = get_project_by_id(project_id)
    items = get_presupuesto_by_project(project_id)
    total_general = get_budget_total(project_id)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm
    )

    title_style, subtitle_style, section_style, normal, small = base_styles()

    story = []

    story.append(Paragraph("Presupuesto de Obra", title_style))
    story.append(Paragraph("Documento generado desde CubiChile.", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(project_table(project))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Detalle de presupuesto", section_style))

    table_data = [
        ["Ítem", "Partida", "Cantidad", "Unidad", "P. Unitario", "Total"]
    ]

    for index, item in enumerate(items, 1):
        cub_id, tipo, volumen, unidad, precio_unitario, total, item_created_at = item
        unidad_txt = unidad_visible(unidad)

        table_data.append([
            str(index),
            Paragraph(tipo or "", small),
            f"{float(volumen or 0):.2f}",
            unidad_txt,
            format_clp(precio_unitario),
            format_clp(total)
        ])

    if not items:
        table_data.append(["-", "Sin partidas registradas", "-", "-", "-", "-"])

    budget_table = Table(
        table_data,
        colWidths=[1.2 * cm, 6.2 * cm, 2.2 * cm, 1.6 * cm, 3 * cm, 3 * cm]
    )

    budget_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 6),

        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
    ]))

    story.append(budget_table)
    story.append(Spacer(1, 16))

    total_table = Table(
        [["TOTAL PRESUPUESTO", format_clp(total_general)]],
        colWidths=[18 * cm, 6 * cm]
    )

    total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 13),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))

    story.append(total_table)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def export_informe_completo_pdf(project_id, filepath):
    project = get_project_by_id(project_id)
    cubicaciones = get_cubicaciones_by_project(project_id)
    presupuesto_items = get_presupuesto_by_project(project_id)
    total_general = get_budget_total(project_id)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=landscape(A4),
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm
    )

    title_style, subtitle_style, section_style, normal, small = base_styles()

    story = []

    story.append(Paragraph("Informe Técnico de Cubicaciones y Presupuesto", title_style))
    story.append(Paragraph("Documento generado automáticamente desde CubiChile.", subtitle_style))
    story.append(Spacer(1, 8))

    story.append(project_table(project))
    story.append(Spacer(1, 14))

    total_partidas = len(cubicaciones)
    total_presupuesto = format_clp(total_general)

    resumen_data = [
        ["Partidas registradas", str(total_partidas)],
        ["Total presupuesto", total_presupuesto],
        ["Estado", "Borrador / revisión técnica"]
    ]

    resumen_table = Table(resumen_data, colWidths=[6 * cm, 11 * cm])
    resumen_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F8FAFC")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(Paragraph("1. Resumen general", section_style))
    story.append(resumen_table)

    story.append(Paragraph("2. Detalle de cubicaciones", section_style))

    cub_table_data = [["Ítem", "Partida", "Medidas", "Cantidad", "Unidad", "Criterio"]]

    for idx, cub in enumerate(cubicaciones, 1):
        cub_id, tipo, largo, ancho, espesor, volumen, unidad, criterio, norma, fecha = cub
        unidad_txt = unidad_visible(unidad)

        if unidad == "m2":
            medidas = f"L: {largo:.2f} m<br/>A: {ancho:.2f} m"
        else:
            medidas = f"L: {largo:.2f} m<br/>A: {ancho:.2f} m<br/>E/P: {espesor:.2f} m"

        cub_table_data.append([
            str(idx),
            Paragraph(tipo or "", small),
            Paragraph(medidas, small),
            f"{volumen:.2f}",
            unidad_txt,
            Paragraph(criterio or norma or "", small)
        ])

    if not cubicaciones:
        cub_table_data.append(["-", "Sin cubicaciones registradas", "-", "-", "-", "-"])

    cub_table = Table(
        cub_table_data,
        colWidths=[1.2 * cm, 5.0 * cm, 4.2 * cm, 2.4 * cm, 1.6 * cm, 11.0 * cm],
        repeatRows=1
    )

    cub_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (3, 1), (4, -1), "RIGHT"),
    ]))

    story.append(cub_table)

    story.append(PageBreak())

    story.append(Paragraph("3. Presupuesto", section_style))

    pres_table_data = [["Ítem", "Partida", "Cantidad", "Unidad", "P. Unitario", "Total"]]

    for idx, item in enumerate(presupuesto_items, 1):
        cub_id, tipo, volumen, unidad, precio_unitario, total, fecha = item
        unidad_txt = unidad_visible(unidad)

        pres_table_data.append([
            str(idx),
            Paragraph(tipo or "", small),
            f"{volumen:.2f}",
            unidad_txt,
            format_clp(precio_unitario),
            format_clp(total)
        ])

    if not presupuesto_items:
        pres_table_data.append(["-", "Sin presupuesto registrado", "-", "-", "-", "-"])

    pres_table = Table(
        pres_table_data,
        colWidths=[1.2 * cm, 8.0 * cm, 3.0 * cm, 2.0 * cm, 4.0 * cm, 4.0 * cm],
        repeatRows=1
    )

    pres_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
    ]))

    story.append(pres_table)
    story.append(Spacer(1, 14))

    total_table = Table(
        [["TOTAL PRESUPUESTO", format_clp(total_general)]],
        colWidths=[18 * cm, 6 * cm]
    )

    total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 13),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))

    story.append(total_table)

    story.append(Paragraph("4. Observación técnica", section_style))
    story.append(Paragraph(
        "Este informe corresponde a una herramienta de apoyo para cubicaciones y presupuesto. "
        "Los resultados deben ser revisados contra planos, especificaciones técnicas, antecedentes del proyecto "
        "y criterios normativos vigentes aplicables. La información generada no reemplaza la revisión profesional.",
        normal
    ))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
