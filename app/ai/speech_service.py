import azure.cognitiveservices.speech as speechsdk

from app.config.azure_config import AzureConfig


class SpeechService:


    @staticmethod
    def transcribe_audio(audio_path):

        speech_config = speechsdk.SpeechConfig(
            subscription=AzureConfig.SPEECH_KEY,
            region=AzureConfig.SPEECH_REGION
        )


        audio_config = speechsdk.audio.AudioConfig(
            filename=audio_path
        )


        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )


        result = recognizer.recognize_once()


        if (
            result.reason
            == speechsdk.ResultReason.RecognizedSpeech
        ):

            return result.text


        return ""