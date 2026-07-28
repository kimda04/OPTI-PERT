import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    AZURE_OPENAI_KEY = os.getenv(
        "AZURE_OPENAI_KEY"
    )

    AZURE_OPENAI_ENDPOINT = os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )