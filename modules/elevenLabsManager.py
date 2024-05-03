from modules.TTS_Manager import TTS_Manager

class ElevenLabsTTS_Manager(TTS_Manager):
    # Voice models available
    MODELS = [
        "eleven_multilingual_v2",
        "eleven_multilingual_v1",
        "eleven_monolingual_v1",
        "eleven_turbo_v2"
    ]

    # Voices available
    VOICES = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Drew": "29vD33N1CtxCmqQRPOHJ",
        "Clyde": "2EiwWnXFnvU5JabPnv8n",
        "Paul": "5Q0t7uMcjvnagumLfvZi",
        "Domi": "AZnzlk1XvdvUeBnXmlld",
        "Dave": "CYw3kZ02Hs0563khs1Fj",
        "Fin": "D38z5RcWu1voky8WS1ja",
        "Sarah": "EXAVITQu4vr4xnSDxMaL",
        "Antoni": "ErXwobaYiN019PkySvjV",
        "Thomas": "GBv7mTt0atIp3Br8iCZE",
        "Charlie": "IKne3meq5aSn9XLyUdCD",
        "George": "JBFqnCBsd6RMkjVDRZzb",
        "Emily": "LcfcDJNUP1GQjkzn1xUU",
        "Elli": "MF3mGyEYCl7XYWbV9V6O",
        "Callum": "N2lVS1w4EtoT3dr4eOWO",
        "Patrick": "ODq5zmih8GrVes37Dizd",
        "Harry": "SOYHLrjzK2X1ezoPC6cr",
        "Liam": "TX3LPaxmHKxFdv7VOQHJ",
        "Dorothy": "ThT5KcBeYPX3keUQqHPh",
        "Josh": "TxGEqnHWrfWFTfGW9XjX",
        "Arnold": "VR6AewLTigWG4xSOukaG",
        "Charlotte": "XB0fDUnXU5powFXDhCwa",
        "Alice": "Xb7hH8MSUJpSbSDYk0k2",
        "Matilda": "XrExE9yKIg1WjnnlVkGX",
        "Matthew": "Yko7PKHZNXotIFUBG7I9",
        "James": "ZQe5CZNOzWyzPSCn5a3c",
        "Joseph": "Zlb1dXrM653N07WRdFW3",
        "Jeremy": "bVMeCyTHy58xNoL34h3p",
        "Michael": "flq6f7yk4E4fJM5XTYuZ",
        "Ethan": "g5CIjZEefAph4nQFvHAz",
        "Chris": "iP95p4xoKVk53GoZ742B",
        "Gigi": "jBpfuIE2acCO8z3wKNLl",
        "Freya": "jsCqWAovK2LkecY7zXl4",
        "Brian": "nPczCjzI2devNBz1zQrb",
        "Grace": "oWAxZDx7w5VEj9dCyTzz",
        "Daniel": "onwK4e9ZLuTAKqWW03F9",
        "Lily": "pFZP5JQG7iQjIQuC4Bku",
        "Serena": "pMsXgVXv3BLzUgSXRplE",
        "Adam": "pNInz6obpgDQGcFmaJgB",
        "Nicole": "piTKgcLEGmPE4e6mEKli",
        "Bill": "pqHfZKP75CvOlQylNhV4",
        "Jessie": "t0jbNlBVZ17f02VDIeMI",
        "Sam": "yoZ06aMxZJJ28mfd3POQ",
        "Glinda": "z9fAnlkpzviPz146aGWa",
        "Giovanni": "zcAOhNBS3c14rBihAFp1",
        "Mimi": "zrHiDhphv9ZnVXBqCLjz"
    }

    # Voices that work better with Italian language
    VOICES_ITA = VOICES

    def __init__(self, API_Key, model="eleven_multilingual_v2", voice_name="Rachel"):
        if voice_name not in self.VOICES:
            raise ValueError("Voice must be one of the following: " +
                             ", ".join(self.VOICES) + ". Got: " + voice_name)
        
        voice = self.VOICES[voice_name]

        super().__init__(API_Key, model, voice)

    # Makes request to TTS API
    def generate_audio(self, input_text, play_audio=False, format="pcm_24000"):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self._voice}"

        headers = {
            "Content-Type": "application/json",
            "xi-api-key": f"{self.API_Key}"    
        }

        querystring = {"output_format": format}

        data = {
            "text": f"{input_text}",
            "model_id": f"{self._model}",
            "voice_settings": {
                "stability": .5,
                "similarity_boost": .7,
                "style": 0,
                "use_speaker_boost": False
            }
        }

        return self.api_call(url, headers, data, play_audio, querystring)