import time
import io
import whisper
import openai
import sounddevice as sd
from scipy.io.wavfile import write
import warnings
import winsound
import pygame
import keyboard
warnings.filterwarnings('ignore')

#OpenAI API key
#openai.api_key = "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" 
openai.api_key = "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"

def play_audio(file_path):
    # Initialize pygame's mixer
    pygame.mixer.init()

    # Load the audio file into pygame's mixer
    pygame.mixer.music.load(file_path)

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Quit the mixer
    pygame.mixer.quit()

messages = [ {"role": "system", "content":  
              """
                Sei uno studente universitario che sta seguendo le lezioni del professore.
                Il professore parlerà di un argomento e tu hai il compito di ascoltarlo attentamente 
                e formulare una domanda di senso compiuto sull'argomento in questione.
                Le domande devono essere pertinenti e non devono essere banali.
                Comunica con il professore dando del Lei ed essere educato.
                Se il professore chiede se hai capito, rispondi con risposte tipo: "Sì, professore" o "No, professore".
                Le domande devono essere coincise e brevi.
                """} ] 

# Set the duration of the recording in seconds
duration = 20.0

# Choose the samplerate
samplerate = 44100

# Load the model
print("Loading the model.")
model = whisper.load_model("small")

while True:
    winsound.Beep(1000, 200)

    # Record audio
    print("Start recording: ")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2)

    end_time = time.time() + duration  # 20 seconds from now

    while True:
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print('--Manual Termination--')
            break  # finish the loop
        if time.time() > end_time:
            break  # finish the loop after 20 seconds

        time_left = int(end_time - time.time())
        print(f'Time left: {time_left} seconds', end='\r')
        time.sleep(0.1)  # a short delay to reduce CPU usage


    # We need to wait for the recording to finish
    sd.wait()

    print("Recording finished.")

    # Save the recording to a file
    print("Saving the recording to a file.")
    write('output.wav', samplerate, recording)

    # Gather model time
    start_time = time.time()

    result = model.transcribe("output.wav")

    print("API Call to GPT-3.5")
    messages.append( 
                {"role": "user", "content": result["text"]}, 
            ) 

    chat = openai.chat.completions.create( 
                model="gpt-3.5-turbo", messages=messages 
            )

    replay = chat.choices[0].message.content
    #print("Replay: ", replay)

    response = openai.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=replay
    )

    audio_file = io.BytesIO(response.content)
    play_audio(audio_file)

    end_time = time.time()

    with open('myfile.txt', 'w', encoding='utf-8') as f:
        f.write(result["text"])

    print("Execution time: ", end_time - start_time, "seconds")

    print("Proceeding? (y/n)")

    choice = input()
    
    if choice == "n":
        break
    else:
        continue