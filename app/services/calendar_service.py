from datetime import datetime, timedelta

from app.services.project_service import get_project


def generate_calendar():

    project = get_project()

    events=[]

    fecha_inicio = datetime.now()


    for activity in project.activities:


        inicio = fecha_inicio + timedelta(
            days=activity.es
        )


        fin = fecha_inicio + timedelta(
            days=activity.ef
        )


        events.append(
            {
                "title":
                activity.name,

                "start":
                inicio.strftime("%Y-%m-%d"),

                "end":
                fin.strftime("%Y-%m-%d"),

                "description":
                activity.description
            }
        )


    return events