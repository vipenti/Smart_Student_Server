from openai import OpenAI
import wave
import tempfile
from modules.STT_Manager import STT_Manager


class Whisper_Manager(STT_Manager):
    def __init__(self, API_Key):
        self.client = OpenAI(api_key=API_Key)

    def transcribe(self, audio):
        # create a temporary file to store the audio data to sent to the model
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
            with wave.open(temp, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2) 
                wav_file.setframerate(44100)  
                wav_file.writeframes(audio)
            
            temp.seek(0)
            
            with open(temp.name, 'rb') as audio_file:
                
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,  # Pass the file object
                    response_format="text",
                    language="it"
                )
        
        return transcription