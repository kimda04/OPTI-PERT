from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from app.services.project_service import get_project


def generate_pdf():
    project = get_project()

    buffer = BytesIO()

    document = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>OPTI-PERT</b>", styles["Title"]))
    elements.append(Paragraph("Sistema Inteligente para Optimización de Proyectos usando PERT/CPM", styles["Heading2"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Proyecto:</b> {project.name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Duración Total:</b> {project.total_duration}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Ruta Crítica:</b> {' → '.join(project.critical_path)}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    data = [[
        "Actividad",
        "TE",
        "ES",
        "EF",
        "LS",
        "LF",
        "Slack"
    ]]

    for activity in project.activities:
        data.append([
            activity.name,
            activity.expected_time,
            activity.es,
            activity.ef,
            activity.ls,
            activity.lf,
            activity.slack
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6C63FF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8)
    ]))

    elements.append(table)

    document.build(elements)

    buffer.seek(0)

    return buffer