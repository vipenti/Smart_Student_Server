from openai import OpenAI
from STT_Manager import STT_Manager

client = OpenAI()

class Whisper_Manager(STT_Manager):
    def __init__(self, API_Key):
        self.API_Key = API_Key

    def transcribe(self, audio):
        
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio, 
            response_format="text",
            language="it"
        )

        return transcription