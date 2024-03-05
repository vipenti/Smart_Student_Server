import time
import whisper
from audioManager import AudioManager
import warnings
import pygame
import numpy as np
from student import Student, Personality, Intelligence
import random
import tempfile

warnings.filterwarnings('ignore')

#OpenAI API key
#openai.api_key = "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" 
API_Key = "YOUR_API_KEY_HERE"

# Initialize pygame's mixer
pygame.mixer.init()

# Load the model
print("Loading the model.")
model = whisper.load_model("small")

recorder = AudioManager()

print("Input the subject of the lesson: ")
subject = input()

# Create a student with random personality and intelligence
random_personality = random.choice(list(Personality))
random_intelligence = random.choice(list(Intelligence))
print(f"Personality: {random_personality.name}\nIntelligence: {random_intelligence.name}\n")

student = Student(random_personality, random_intelligence, subject, API_Key)

default_speaker_filename = "speaker_audio.wav"

while True:
    


    # Record audio
    print("Start recording: ")
    recorder.start()
    print("Recording finished.")

    # Save the recording to a file
    print("Saving the recording to a file.")
    buffer = recorder.save_temp()

    with tempfile.NamedTemporaryFile('wb+', delete=False) as temp:
        buffer.seek(0)
        temp.write(buffer.read())
        temp.seek(0)
        temp_file = temp.name

    # Gather model time
    start_time = time.time()

    print("Transcribing the audio file.")
    result = model.transcribe(temp_file)

    print("API Call to GPT-3.5")
    reply = student.generate_question(result["text"])
    #reply = gpt_manager.generate_response("TEST")
    
    end_time = time.time()
    print("Execution time: ", end_time - start_time, "seconds\n")

    print(f"Student: '{reply}'")

    student.generate_audio(reply)

    with open('myfile.txt', 'w', encoding='utf-8') as f:
        f.write(result["text"])

    print("Proceeding? (y/n)")

    choice = input()
    
    if choice == "y":
        continue
    else:
        break


# Quit the mixer
pygame.mixer.quit()