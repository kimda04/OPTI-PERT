class ContextBuilder:

    @staticmethod
    def build_project_context(project):

        context = """
Eres un asistente especializado exclusivamente en PERT y CPM.

Tu función es analizar proyectos utilizando únicamente
la información proporcionada del proyecto actual.

No inventes actividades ni datos que no existan.

Proyecto actual:

"""

        if not project:
            context += """
No existe ningún proyecto cargado.
"""

            return context


        context += f"""
Duración total del proyecto:
{getattr(project, 'duration', 'No calculada')} días


Actividades:
"""


        for activity in project.activities:

            context += f"""

Actividad:
{activity.name}

Descripción:
{activity.description}

Tiempo optimista:
{activity.optimistic}

Tiempo más probable:
{activity.most_likely}

Tiempo pesimista:
{activity.pessimistic}

Tiempo esperado:
{getattr(activity, 'expected_time', 'No calculado')}

Inicio temprano:
{getattr(activity, 'early_start', 'No calculado')}

Fin temprano:
{getattr(activity, 'early_finish', 'No calculado')}

Inicio tardío:
{getattr(activity, 'late_start', 'No calculado')}

Fin tardío:
{getattr(activity, 'late_finish', 'No calculado')}

Holgura:
{getattr(activity, 'slack', 'No calculada')}

Crítica:
{getattr(activity, 'critical', False)}

Predecesores:
{activity.predecessors}

"""


        if hasattr(project, "critical_path"):

            context += f"""

Ruta crítica:

{project.critical_path}

"""


        context += """

Responde siempre:

- usando los datos del proyecto.
- explicando con lenguaje académico.
- relacionando las respuestas con PERT/CPM.
"""


        return context