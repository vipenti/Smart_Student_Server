from celery import Celery
from student import Student, Personality, Intelligence, Interest, Happyness
import whisper
import pyttsx3
import base64
import io
import os
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile

# Configura Celery per il task broker
app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def generate_audio_response_task(audio_data, subject, personality, intelligence, interest, happyness):

    # Decodifica i dati audio in base64 e li converte in un AudioSegment
    audio_bytes = base64.b64decode(audio_data)
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")

    # Salva l'audio come file temporaneo in un buffer per Whisper
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)

    # Carica i dati audio come array numpy per Whisper
    sample_rate, audio_array = wavfile.read(buffer)
    audio_array = audio_array.astype(np.float32) / 32768.0  # Normalizza a float32

    # Converte i tratti di personalità in oggetti Enum
    personality = Personality(personality)
    intelligence = Intelligence(intelligence)
    interest = Interest(interest)
    happyness = Happyness(happyness)

    # Inizializza lo studente con i tratti convertiti
    student = Student(subject, personality, intelligence, interest, happyness)

    # Utilizza Whisper per trascrivere l’audio
    transcriber = whisper.load_model("base")
    transcription = transcriber.transcribe(audio_array, language="en")["text"]
    print(f"Transcribed test: {transcription}")

    # Genera la risposta dello studente utilizzando il modello LLaMA
    response_text = student.generate_response(transcription)

    # Converte la risposta in audio con pyttsx3, salvando su file temporaneo
    tts_engine = pyttsx3.init()
    temp_audio_path = "response_audio.wav"
    tts_engine.save_to_file(response_text, temp_audio_path)
    tts_engine.runAndWait()

    # Leggi il file temporaneo e converti l'audio in base64
    with open(temp_audio_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

    # Rimuovi il file temporaneo
    os.remove(temp_audio_path)

    return audio_base64
