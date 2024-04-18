from modules.textGenerationManager import TextGenerationManager
from modules.TTS_Manager import TTS_Manager

# TODO Create template method pattern design to decouple completions model and voice model

class Speaker:
    def __init__(self, text_manager, tts_manager, starting_prompt):        
        self.starting_prompt = starting_prompt

        self.text_manager = text_manager

        self.text_manager.starting_prompt = starting_prompt
        
        self.tts_manager = tts_manager

    def generate_response(self, message):
        return self.text_manager.generate_response_history(message)

    def generate_audio(self, message, play_audio=True, format="mp3"):
        return self.tts_manager.generate_audio(message, play_audio, format)