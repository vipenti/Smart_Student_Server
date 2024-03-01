import time
import whisper
from audioManager import AudioManager
import warnings
import pygame
from openAI_TTS_Manager import OpenAI_TTS_Manager
from chatGPT_Manager import ChatGPT_Manager

warnings.filterwarnings('ignore')

#OpenAI API key
#openai.api_key = "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" 
API_Key = "YOUR_API_KEY_HERE"

# Initialize pygame's mixer
pygame.mixer.init()

starting_prompt ="""
                Sei uno studente universitario che sta seguendo le lezioni del professore.
                Il professore parlerà di un argomento e tu hai il compito di ascoltarlo attentamente 
                e formulare una domanda di senso compiuto sull'argomento in questione.
                Le domande devono essere pertinenti e non devono essere banali.
                Comunica con il professore dando del Lei ed essere educato.
                Se il professore chiede se hai capito, rispondi con risposte tipo: "Sì, professore" o "No, professore".
                Le domande devono essere coincise e brevi.
                """

# Initialize the OpenAI TTS Manager
tts_manager = OpenAI_TTS_Manager(API_Key)

# Initialize the ChatGPT Manager
gpt_manager = ChatGPT_Manager(API_Key, starting_prompt= starting_prompt)

# Load the model
print("Loading the model.")
model = whisper.load_model("small")

recorder = AudioManager()

default_speaker_filename = "speaker_audio.wav"

while True:

    # Record audio
    print("Start recording: ")
    recorder.start()
    print("Recording finished.")

    # Save the recording to a file
    print("Saving the recording to a file.")
    #recorder.save(default_speaker_filename)
    buffer = recorder.save_temp()

    # Gather model time
    start_time = time.time()

    result = model.transcribe(buffer)

    print("API Call to GPT-3.5")
    reply = gpt_manager.generate_response_history(result["text"])
    #reply = gpt_manager.generate_response("TEST")
    
    end_time = time.time()
    print("Execution time: ", end_time - start_time, "seconds\n")

    print(f"Student: '{reply}'")

    # tts_manager.generate_audio(reply)

    # with open('myfile.txt', 'w', encoding='utf-8') as f:
    #     f.write(result["text"])

    print("Proceeding? (y/n)")

    choice = input()
    
    if choice == "n":
        break
    else:
        continue


# Quit the mixer
pygame.mixer.quit()