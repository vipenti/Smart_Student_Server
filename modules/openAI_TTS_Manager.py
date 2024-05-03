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
        super().__init__(API_Key, model, voice)

    # Makes request to OpenAI TTS API, saves response as stream of bytes, and calls play_audio method from AudioManager on the stream
    # This allows for audio streaming and therefore real-time audio generation
    def generate_audio(self, input_text, play_audio=True, format="mp3"):
        url = "https://api.openai.com/v1/audio/speech"

        headers = {"Authorization": 'Bearer ' + self.API_Key}

        data = {
            "model": self.model,
            "input": input_text,
            "voice": self.voice,
            "response_format": format,
        }

        return self.api_call(url, headers, data, play_audio)
