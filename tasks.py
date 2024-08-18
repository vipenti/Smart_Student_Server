from config import create_app
from celery import shared_task 
from flask import jsonify, Response
import tempfile
import whisper
import random
import base64
import os
import io
import numpy as np
import wave

from modules.openAI_TTS_Manager import OpenAI_TTS_Manager
from modules.chatGPT_Manager import ChatGPT_Manager
from student import Student, Personality, Intelligence


flask_app = create_app()
celery_app = flask_app.extensions["celery"]

print("Loading the model.")
model = whisper.load_model("small")

student = None

@shared_task(ignore_result=True)
def create_student(subject, openAI_key):
    global student

    # Create a student with random personality, intelligence and voice
    # random_personality = random.choice(list(Personality))
    # random_intelligence = random.choice(list(Intelligence))
    random_personality = Personality.CONFIDENT
    random_intelligence = Intelligence.HIGH
    voice = random.choice(OpenAI_TTS_Manager.VOICES_ITA)

    tts_model = OpenAI_TTS_Manager(openAI_key, voice=voice)
    completions_model = ChatGPT_Manager(openAI_key)

    student = Student(random_personality, random_intelligence, subject, completions_model, tts_model)
    return 

@shared_task(bind=True, ignore_result=False)
def generate_spoken_question(self, audio_data):
    # create a temporary file to store the audio data to sent to the model
    with tempfile.NamedTemporaryFile('wb+', delete=False) as temp:
        temp.write(audio_data)
        temp.seek(0)
    
    print("[Whisper] Transcribing audio")
    transcription = model.transcribe(temp.name)

    print("Transcription: ", transcription["text"])

    print("[Chat Completions] Generating response")
    reply = student.generate_response(transcription["text"], check_correlation=False)

    # if transcript is empty, return an error
    if reply is None:
        self.update_state(state='FAILURE')
        return "Studente rimasto in silenzio"

    print("[Text-to-Speech] Generating audio")

    student.voice = random.choice(OpenAI_TTS_Manager.VOICES_ITA)
    # response = Response(student.generate_audio(reply, play_audio=False, format="pcm"), status=200, mimetype='audio/wav')
    response = student.generate_audio(reply, play_audio=False, format="pcm")
    # response = audio_data

    response = base64.b64encode(response.getvalue()).decode('utf-8')

    print("[Response] Sending response")
    return response

@shared_task(bind=True, ignore_result=False)
def test_task(self, duration = 1, sample_rate = 16000):
    
    # Number of samples
    num_samples = duration * sample_rate
    
    # Generate random audio data
    audio_data = np.random.randint(-32768, 32767, num_samples, dtype=np.int16)
    
    buffer = io.BytesIO()

    # Write the audio data to a PCM file
    with wave.open(buffer, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    
    buffer.seek(0)
    encoded_audio = base64.b64encode(buffer.getvalue()).decode('utf-8')

    print("[TEST] Sending response")
    return encoded_audio