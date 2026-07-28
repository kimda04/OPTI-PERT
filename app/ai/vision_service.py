from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from app.config.azure_config import AzureConfig


class VisionService:

    @staticmethod
    def extract_text(image_path):

        client = ImageAnalysisClient(
            endpoint=AzureConfig.VISION_ENDPOINT,
            credential=AzureKeyCredential(
                AzureConfig.VISION_KEY
            )
        )

        with open(image_path, "rb") as image_file:

            image_data = image_file.read()


        result = client.analyze(
            image_data=image_data,
            visual_features=[
                VisualFeatures.READ
            ]
        )


        extracted_text = []


        if result.read:

            for block in result.read.blocks:

                for line in block.lines:

                    extracted_text.append(
                        line.text
                    )


        return "\n".join(
            extracted_text
        )