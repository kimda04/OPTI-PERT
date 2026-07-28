from openai import OpenAI

from app.config.azure_config import AzureConfig


class OpenAIService:

    client = OpenAI(
        api_key=AzureConfig.AZURE_OPENAI_API_KEY,
        base_url=AzureConfig.AZURE_OPENAI_ENDPOINT
    )


    @staticmethod
    def ask(question, project_context):

        prompt = f"""
Eres un experto universitario en Investigación Operativa.

Tu especialidad es exclusivamente:

- PERT
- CPM
- Ruta crítica
- Gestión de proyectos


Reglas importantes:

1. Analiza solamente la información del proyecto entregado.
2. No inventes actividades.
3. No inventes duraciones.
4. No agregues datos externos.
5. Si la información no existe, indícalo claramente.


Información actual del proyecto:

{project_context}


Pregunta del usuario:

{question}


Responde de forma:

- técnica
- clara
- organizada
- orientada a la toma de decisiones.
"""


        response = OpenAIService.client.responses.create(
            model=AzureConfig.AZURE_OPENAI_DEPLOYMENT,
            input=prompt
        )


        return response.output_text