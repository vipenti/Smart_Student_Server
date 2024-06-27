from config import create_app
from celery import shared_task 
from time import sleep

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

@shared_task(ignore_result=False)
def transcribe_audio(model, audio):
    return model.transcribe(audio.name)

@shared_task(ignore_result=False)
def generate_text(student, prompt):
    return student.generate_response(prompt)

@shared_task(ignore_result=False)
def generate_audio(student, text):
    return student.generate_audio(text, play_audio=False, format="pcm")