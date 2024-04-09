from modules.audioManager import AudioManager


class TTS_Manager:
    # Voice models available
    MODELS = []

    # Voices available
    VOICES = []

    # Voices that work better with Italian language
    VOICES_ITA = []

    def __init__(self, API_Key, model, voice):
        self.API_Key = API_Key  # API Key
        self._model = model      # TTS model
        self._voice = voice      # TTS voice
        self.recorder = AudioManager()  # AudioManager object to play the audio

    # Makes request to TTS API
    def generate_audio(self, input_text):
        pass
    
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