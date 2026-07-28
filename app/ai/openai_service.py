from openai import OpenAI

from app.config.azure_config import AzureConfig


class OpenAIService:

    client = OpenAI(
        api_key=AzureConfig.AZURE_OPENAI_API_KEY,
        base_url=AzureConfig.AZURE_OPENAI_ENDPOINT
    )

    @staticmethod
    def ask(context, question):

        response = OpenAIService.client.chat.completions.create(
            model=AzureConfig.AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response.choices[0].message.content