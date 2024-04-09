import requests
import io
from modules.audioManager import AudioManager
from modules.TTS_Manager import TTS_Manager

class OpenAI_TTS_Manager(TTS_Manager):
    # Voice models available from OpenAI as of 8 March 2024
    MODELS = [
        "tts-1",
        "tts-1-hd",
    ]

    # Voices available from OpenAI as of 8 March 2024
    VOICES = [
        "nova",
        "alloy",
        "echo",
        "fable",
        "onyx",
        "shimmer"
    ]

    # Voices that work better with Italian language
    VOICES_ITA = [
        "echo",
        "fable",
        "onyx"
    ]

    def __init__(self, API_Key, model='tts-1', voice='nova'):
        if model not in self.MODELS:
            raise ValueError("Model must be one of the following: " +
                             ", ".join(self.MODELS) + ". Got: " + model)

        if voice not in self.VOICES:
            raise ValueError("Voice must be one of the following: " +
                             ", ".join(self.VOICES) + ". Got: " + voice)
        
        
        super().__init__(API_Key, model, voice)

    # Makes request to OpenAI TTS API, saves response as stream of bytes, and calls play_audio method from AudioManager on the stream
    # This allows for audio streaming and therefore real-time audio generation
    def generate_audio(self, input_text):
        url = "https://api.openai.com/v1/audio/speech"

        headers = {"Authorization": 'Bearer ' + self.API_Key}

        data = {
            "model": self.model,
            "input": input_text,
            "voice": self.voice,
            "response_format": "opus",
        }

        # Make the request to OpenAI TTS Endpoint
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            if response.status_code == 200:
                buffer = io.BytesIO()

                # Write the response to the bytes buffer
                for chunk in response.iter_content(chunk_size=1024):
                    buffer.write(chunk)

                buffer.seek(0)

                # Play the audio from the buffer
                self.recorder.play_audio(buffer)

                return buffer
            else:
                # Print the error message if the request was not successful
                print(f"Error: {response.status_code} - {response.text}")
                return None
