import time
import whisper
import warnings
import json
import random
import tempfile
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
from modules.audioManager import AudioManager
from student import Student, Personality, Intelligence

#warnings.filterwarnings('ignore')

# Carica Whisper e Hugging Face
print("Loading Whisper and Hugging Face model.")
model = whisper.load_model("small")
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")
text_model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")

# Inizializza AudioManager e TTS
recorder = AudioManager()
tts_model = pyttsx3.init()
tts_model.setProperty('rate', 150)

# Input utente
print("Input the subject of the lesson: ")
subject = input()

student = Student(Personality.CONFIDENT, Intelligence.HIGH, subject)

while True:
    print("[Recording] Started recording: ")
    recorder.start(voice_activity_detection=True)

    print("[Saving] Saving the recording to a file.")
    buffer = recorder.save_temp()
    with tempfile.NamedTemporaryFile('wb+', delete=False) as temp:
        buffer.seek(0)
        temp.write(buffer.read())
        temp.seek(0)
        temp_file = temp.name

    start_time = time.time()
    print("[Speech-to-Text] Transcribing the audio file.")
    result = model.transcribe(temp_file)

    print("[Text Generation] Generating response with Hugging Face model.")
    inputs = tokenizer(result["text"], return_tensors="pt")
    outputs = text_model.generate(inputs.input_ids, max_length=150)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)

    end_time = time.time()
    print("Execution time: ", end_time - start_time, "seconds\n")

    if reply:
        print(f"Student: '{reply}'")
        tts_model.say(reply)
        tts_model.runAndWait()

    print("Proceeding? (y/n)")
    choice = input()
    if choice != "y":
        break
