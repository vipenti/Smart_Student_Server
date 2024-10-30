from config import create_app
from celery import shared_task 
import random
import base64
import io
import numpy as np
import wave

from student import Student, Personality, Intelligence, Interest, Happyness
from speaking_interface import Speaker
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

# Caricamento del modello Hugging Face
print("Loading the Hugging Face model.")
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")
text_model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")

# Inizializzazione del sistema TTS locale
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Velocità del parlato

student = None

@shared_task(ignore_result=True)
def create_student(subject):
    global student

    # Creazione dello studente con valori casuali per le caratteristiche
    random_personality = random.choice(list(Personality))
    random_intelligence = random.choice(list(Intelligence))
    random_interest = random.choice(list(Interest))
    random_happyness = random.choice(list(Happyness))

    # Instanzia lo studente con i valori casuali e i nuovi manager
    student = Student(
        personality=random_personality,
        intelligence=random_intelligence,
        interest=random_interest,
        happyness=random_happyness,
        subject=subject,
    )
    return 

@shared_task(bind=True, ignore_result=False)
def generate_written_question(self, audio_data):
    # Trascrizione dell'audio con Whisper locale
    print("[Whisper] Transcribing audio")
    transcription = student.transcribe(audio_data)  # Usa Whisper locale

    print("Transcription: ", transcription)

    print("[Chat Completion] Generating response")
    reply = student.generate_response(transcription, check_correlation=False)

    # Se la risposta è vuota, restituisce un errore
    if reply is None:
        self.update_state(state='FAILURE')
        return "Studente rimasto in silenzio"

    return reply


@shared_task(bind=True, ignore_result=False)
def generate_spoken_question(self, audio_data):
    # Richiama la funzione di generazione della domanda scritta
    result = generate_written_question.delay(audio_data)
    reply = result.get()
   
    print("[Text-to-Speech] Generating audio")

    # Genera l'audio della risposta
    buffer = io.BytesIO()
    tts_engine.save_to_file(reply, buffer)
    buffer.seek(0)

    # Codifica la risposta audio in base64
    response = base64.b64encode(buffer.getvalue()).decode('utf-8')

    print("[Response] Sending response")
    return response

@shared_task(bind=True, ignore_result=False)
def test_task(self, duration=1, sample_rate=16000):
    # Numero di campioni
    num_samples = duration * sample_rate
    
    # Generazione di dati audio casuali
    audio_data = np.random.randint(-32768, 32767, num_samples, dtype=np.int16)
    
    buffer = io.BytesIO()

    # Scrive i dati audio in un file PCM
    with wave.open(buffer, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 byte per campione
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    
    buffer.seek(0)
    encoded_audio = base64.b64encode(buffer.getvalue()).decode('utf-8')

    print("[TEST] Sending response")
    return encoded_audio
