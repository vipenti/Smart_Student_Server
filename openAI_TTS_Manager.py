import requests
import soundfile as sf
import io
from audioManager import AudioManager

OPENAI_VOICES = [
    "nova",
    "alloy",
    "echo",
    "fable",
    "onyx",
    "shimmer"
]

OPENAI_VOICES_ITA = [
    "nova",
    "echo",
    "fable",
    "onyx",
    "shimmer"
]   

class OpenAI_TTS_Manager:
    def __init__(self, API_Key, model='tts-1', voice='nova'):
        self.API_Key = API_Key
        self.model = model
        self.voice = voice
        self.recorder = AudioManager()
    
    # Makes request to OpenAI TTS API, saves response as stream of bytes, and calls play_audio method from AudioManager on the stream
    def generate_audio(self, input_text):
        url = "https://api.openai.com/v1/audio/speech"

        headers = { "Authorization": 'Bearer ' + self.API_Key }

        data = {
            "model": self.model,
            "input": input_text,
            "voice": self.voice,
            "response_format": "opus",
        }

        with requests.post(url, headers=headers, json=data, stream=True) as response:
            if response.status_code == 200:
                buffer = io.BytesIO()

                for chunk in response.iter_content(chunk_size=1024):
                    buffer.write(chunk)

                buffer.seek(0)

                self.recorder.play_audio(buffer)
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None