import openai
import io
import tempfile
from modules.STT_Manager import STT_Manager


class Whisper_Manager(STT_Manager):
    def __init__(self, API_Key):
        openai.api_key = API_Key

    def transcribe(self, audio):
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio, 
            response_format="text",
            language="it"
        )

        return transcription