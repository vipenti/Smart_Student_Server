from celery import Celery
from student import Student, Personality, Intelligence, Interest, Happyness
import whisper
import pyttsx3
import base64
import os
import torch
import torchaudio
from silero import silero_tts

# Configura Celery per il task broker
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def generate_audio_response_task(audio_data, subject, personality, intelligence, interest, happyness):

    output_path = os.path.join(os.path.dirname(__file__), "sounds/to_transcribe.wav")

    with open(output_path, "wb") as audio_file:
        audio_file.write(base64.b64decode(audio_data))

    model = whisper.load_model("base")

    transcription = model.transcribe(output_path)['text']
    print(f"Transcribed test: {transcription}")
    os.remove(output_path)

    personality = Personality(personality)
    intelligence = Intelligence(intelligence)
    interest = Interest(interest)
    happyness = Happyness(happyness)

    student = Student(subject, personality, intelligence, interest, happyness)
    response_text = student.generate_response(transcription)

    temp_audio_path = os.path.join(os.path.dirname(__file__), "tmp/response_audio.wav")
    generate_audio(response_text, temp_audio_path)

    with open(temp_audio_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

    #os.remove(temp_audio_path)

    return audio_base64


def generate_audio(text, path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    language = 'en'
    speaker = 'random'
    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                         model='silero_tts',
                                         language=language,
                                         speaker='v3_en')

    audio = model.apply_tts(text=text, speaker=speaker)
    torchaudio.save(path, torch.tensor(audio).unsqueeze(0), 48000)

