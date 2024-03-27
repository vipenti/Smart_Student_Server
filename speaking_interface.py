from modules.chatGPT_Manager import ChatGPT_Manager
from modules.openAI_TTS_Manager import OpenAI_TTS_Manager

# TODO Create template method pattern design to decouple completions model and voice model

class Speaker:
    def __init__(self, API_key, voice, completions_model, voice_model, starting_prompt):
        self.starting_prompt = starting_prompt

        self.gpt_manager = ChatGPT_Manager(
            API_key, model=completions_model, starting_prompt=self.starting_prompt)
        
        self.tts_manager = OpenAI_TTS_Manager(
            API_key, model=voice_model, voice=voice)

    def generate_response(self, message):
        return self.gpt_manager.generate_response_history(message)

    def generate_audio(self, message):
        return self.tts_manager.generate_audio(message)

    @property
    def voice(self):
        return self.tts_manager.voice

    @voice.setter
    def voice(self, value):
        if value in OpenAI_TTS_Manager.OPENAI_VOICES:
            self.tts_manager.voice = value
        else:
            raise ValueError("Voice must be one of the following: " +
                             ", ".join(OpenAI_TTS_Manager.OPENAI_VOICES) + ". Got: " + value)
