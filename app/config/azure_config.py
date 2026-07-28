import os


class AzureConfig:

    SPEECH_KEY = os.getenv(
        "AZURE_SPEECH_KEY"
    )

    SPEECH_REGION = os.getenv(
        "AZURE_SPEECH_REGION"
    )

    VISION_KEY = os.getenv(
        "AZURE_VISION_KEY"
    )

    VISION_ENDPOINT = os.getenv(
        "AZURE_VISION_ENDPOINT"
    )
    
    AZURE_OPENAI_API_KEY = os.getenv(
        "AZURE_OPENAI_API_KEY"
    )

    AZURE_OPENAI_ENDPOINT = os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )

    AZURE_OPENAI_DEPLOYMENT = os.getenv(
        "AZURE_OPENAI_DEPLOYMENT"
    )