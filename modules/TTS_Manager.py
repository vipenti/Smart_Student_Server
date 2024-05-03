from modules.audioManager import AudioManager
import requests
import io

class TTS_Manager:
    # Voice models available
    MODELS = []

    # Voices available
    VOICES = []

    # Voices that work better with Italian language
    VOICES_ITA = []

    def __init__(self, API_Key, model, voice):
        if model not in self.MODELS:
            raise ValueError("Model must be one of the following: " +
                             ", ".join(self.MODELS) + ". Got: " + model)
        
        if(type(self.VOICES) is dict):
            if voice not in list(self.VOICES.values()):
                raise ValueError("Voice must be one of the following: " +
                             ", ".join(self.VOICES) + ". Got: " + voice)
        else:
            if voice not in self.VOICES:
                raise ValueError("Voice must be one of the following: " +
                             ", ".join(self.VOICES) + ". Got: " + voice)

        self.API_Key = API_Key  # API Key
        self._model = model      # TTS model
        self._voice = voice      # TTS voice
        self.recorder = AudioManager()  # AudioManager object to play the audio

    # Makes request to TTS API
    def generate_audio(self, input_text, play_audio=True, format=None):
        pass

    def api_call(self, url, headers, data, play_audio=False, params=None):
        with requests.post(url, json=data, headers=headers, params=params, stream=True) as response:
            if response.status_code == 200:
                buffer = io.BytesIO()

                for chunk in response.iter_content(chunk_size=1024):
                    buffer.write(chunk)
                
                buffer.seek(0)

                # Play the audio from the buffer
                if play_audio:
                    self.recorder.play_audio(buffer)

                return buffer

            else:
                 # Print the error message if the request was not successful
                print(f"Error: {response.status_code} - {response.text}")
                return None
    
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, value):
        if value not in self.MODELS:
            raise ValueError("Model must be one of the following: " +
                             ", ".join(self.MODELS) + ". Got: " + value)
        else:
            self._model = value
    
    @property
    def voice(self):
        return self._voice
    
    @voice.setter
    def voice(self, value):
        if value not in self.VOICES:
            raise ValueError("Voice must be one of the following: " +
                             ", ".join(self.VOICES) + ". Got: " + value)
        else:
            self._voice = value