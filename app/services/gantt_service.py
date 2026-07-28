from io import BytesIO
import pandas as pd
import plotly.express as px
from app.services.project_service import get_project


def build_gantt_figure():

    project = get_project()

    if not project.activities:
        return None

    data = []

    for activity in project.activities:
        data.append({
            "Actividad": activity.name,
            "Inicio": activity.es,
            "Fin": activity.ef,
            "Ruta": "Sí" if activity.name in project.critical_path else "No"
        })

    df = pd.DataFrame(data)

    fig = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fin",
        y="Actividad",
        color="Ruta",
        color_discrete_map={
            "Sí": "#DC2626",
            "No": "#7C4DFF"
        }
    )

    fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        template="plotly_white",
        height=600,
        title="Cronograma del proyecto - Gantt",
        xaxis_title="Días",
        yaxis_title="Actividades",
        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40
        )
    )

    return fig


def generate_gantt():

    fig = build_gantt_figure()

    if fig is None:
        return ""

    return fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )


def export_gantt_png():

    fig = build_gantt_figure()

    buffer = BytesIO()

    fig.write_image(
        buffer,
        format="png",
        width=1400,
        height=700,
        scale=2
    )

    buffer.seek(0)

    return buffer