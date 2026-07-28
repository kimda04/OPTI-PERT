from app.services.project_service import get_project


class PertContextService:

    @staticmethod
    def generate_context():

        project = get_project()

        context = """
Proyecto OPTI-PERT

Información actual del proyecto:

"""

        context += "Actividades:\n\n"

        for activity in project.activities:

            context += f"""
Actividad: {activity.name}
Descripción: {activity.description}
Tiempo optimista: {activity.optimistic}
Tiempo probable: {activity.most_likely}
Tiempo pesimista: {activity.pessimistic}
Predecesores: {", ".join(activity.predecessors)}

"""

        return context