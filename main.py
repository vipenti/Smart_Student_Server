import time
import whisper
from modules.audioManager import AudioManager
import warnings
import json
from student import Student, Personality, Intelligence
from modules.openAI_TTS_Manager import OpenAI_TTS_Manager
import random
import tempfile

warnings.filterwarnings('ignore')

with open('configs/API_key.json') as config_file:
    data = json.load(config_file)

# OpenAI API key
API_Key = data['API_KEY']

# Load the model
print("Loading the model.")
model = whisper.load_model("small")

recorder = AudioManager() # AudioManager object to record the audio

# Ask the user for the subject of the lesson
print("Input the subject of the lesson: ")
subject = input()

# Create a student with random personality, intelligence and voice
# random_personality = random.choice(list(Personality))
# random_intelligence = random.choice(list(Intelligence))
voice = random.choice(OpenAI_TTS_Manager.OPENAI_VOICES_ITA)
# print(f"Personality: {random_personality.name}\nIntelligence: {random_intelligence.name}\nVoice: {voice}")

student = Student(Personality.CONFIDENT, Intelligence.HIGH, subject, API_Key, voice)

f = open

while True:
    # Record audio
    print("[Recording] Started recording: ")
    recorder.start(voice_activity_detection= True)

    # Save the recording to a byte buffer
    print("[Saving] Saving the recording to a file.")
    buffer = recorder.save_temp()

    # Save the recording to a temporary file
    with tempfile.NamedTemporaryFile('wb+', delete=False) as temp:
        buffer.seek(0)
        temp.write(buffer.read())
        temp.seek(0)
        temp_file = temp.name

    # Gather model time
    start_time = time.time()

    print("[Speech-to-Text] Transcribing the audio file.")
    result = model.transcribe(temp_file)

    print("[Text Generation] API Call to OpenAI Chat")
    reply = student.generate_response(result["text"])
    
    # DEBUG ONLY - Print calls and models time
    end_time = time.time()
    print("Execution time: ", end_time - start_time, "seconds\n")

    # If the reply is valid then play the audio
    if reply:
        print(f"Student: '{reply}'")

        # Generate audio from the reply
        student.generate_audio(reply)

        # DEBUG ONLY - Save the reply to a file
        # with open('myfile.txt', 'w', encoding='utf-8') as f:
        #     f.write(result["text"])

    print("Proceeding? (y/n)")

    choice = input()
    
    if choice == "y":
        continue
    else:
        break