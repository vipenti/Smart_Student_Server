from celery import Celery
from student import Student, Personality, Intelligence, Interest, Happiness
import whisper
import pyttsx3
import base64
import os
import torch
import torchaudio
from silero import silero_tts

# Configura Celery per il task broker
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Global model variable to reduce the loading time each time a task is executed
model = None

model = whisper.load_model("base")
print("Model loaded")

@app.task
def generate_text_response_task(audio_data, subject, personality, intelligence, interest, happiness):
    global model

    output_dir = os.path.join(os.path.dirname(__file__), "sounds")
    output_path = os.path.join(output_dir, "to_transcribe.wav")

    # Check if the folder exists, otherwise create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the audio file in base64 format
    with open(output_path, "wb") as audio_file:
        audio_file.write(base64.b64decode(audio_data))

    #model = whisper.load_model("base")

    # Transcribe the audio
    transcription = model.transcribe(output_path)['text']
    print(f"Transcribed test: {transcription}")
    # os.remove(output_path)

    # Create the student object with the given parameters
    personality = Personality(personality)
    intelligence = Intelligence(intelligence)
    interest = Interest(interest)
    happiness = Happiness(happiness)

    student = Student(subject, personality, intelligence, interest, happiness)

    # Generate the response text
    response_text = student.generate_response(transcription)

    return response_text

@app.task
def generate_audio_response_task(audio_data, subject, personality, intelligence, interest, happiness):
    # Call the text response task and wait for the result
    response_task = generate_text_response_task.delay(audio_data, subject, personality, intelligence, interest, happiness)
    response_text = response_task.get()

    output_dir = os.path.join(os.path.dirname(__file__), "tmp")

    # Check if the folder exists, otherwise create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the audio file
    temp_audio_path = os.path.join(output_dir, "response_audio.wav")
    generate_audio(response_text, temp_audio_path)

    with open(temp_audio_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

    #os.remove(temp_audio_path)

    # Return the response text and the audio file in base64 format
    response = {
        "text": response_text,
        "audio": audio_base64
    }

    return response
    
# Function to generate audio from text using Silero TTS
def generate_audio(text, path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    language = 'en'
    speaker = 'random'

    # Load the model
    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                         model='silero_tts',
                                         language=language,
                                         speaker='v3_en')
    # Apply the TTS model
    audio = model.apply_tts(text=text, speaker=speaker)

    # Save the audio file in 44100 Hz because it's more convenient for Unity
    torchaudio.save(path, torch.tensor(audio).unsqueeze(0), 44100)

