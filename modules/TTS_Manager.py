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
        self.model = model      # TTS model
        self.voice = voice      # TTS voice
        self.recorder = AudioManager()  # AudioManager object to play the audio

    # Makes request to TTS API
    def generate_audio(self, input_text):
        pass
