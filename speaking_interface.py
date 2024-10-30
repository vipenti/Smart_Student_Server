from transformers import AutoModelForCausalLM, AutoTokenizer
import pyttsx3

class TextGenerationManager:
    def __init__(self, model_name="EleutherAI/gpt-neo-2.7B"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response_history(self, message):
        inputs = self.tokenizer(message, return_tensors="pt")
        outputs = self.model.generate(inputs.input_ids, max_length=150)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

class TTS_Manager:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)

    def generate_audio(self, message, play_audio=True, format="a"):
        if play_audio:
            self.tts_engine.say(message)
            self.tts_engine.runAndWait()
            
class Speaker:
    def __init__(self, starting_prompt):        
        self.starting_prompt = starting_prompt

        # Inizializza i manager per Hugging Face e TTS locale
        self.text_manager = TextGenerationManager()
        self.tts_manager = TTS_Manager()

        self.text_manager.starting_prompt = starting_prompt

    def generate_response(self, message):
        return self.text_manager.generate_response_history(message)

    def generate_audio(self, message, play_audio=True, format="a"):
        return self.tts_manager.generate_audio(message, play_audio, format)
