from enum import Enum
from chatGPT_Manager import ChatGPT_Manager
from openAI_TTS_Manager import OpenAI_TTS_Manager, voices
import random 

starting_prompt ="""
                Sei uno studente universitario che sta seguendo le lezioni del professore sulla materia {subject}.
                Il professore parlerà di un argomento ({subject}) e tu hai il compito di ascoltarlo attentamente 
                e formulare una domanda di senso compiuto sull'argomento in questione.
                Se il professore cambia materia o argomento, puntualizza dicendo frasi tipo 'Scusi prof, ma non stavamo parlando di...'.
                Le domande devono essere pertinenti e non devono essere banali.
                Le tue domande devono essere di difficoltà {difficulty} su 3.
                Comunica con il professore dando del Lei ed essere educato.
                Se il professore chiede se hai capito, rispondi con risposte tipo: "Sì, prof" o "No, prof".
                Le domande devono essere coincise e brevi.
                Rispondi solamente con le domande.
                """

class Personality(Enum):
    SILENT = 1
    SHY = 2
    TALKATIVE = 3
    OUTGOING = 4
    CONFIDENT = 5    

class Intelligence(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Student:
    def __init__(self, personality, intelligence, subject, API_Key):
        self.personality = personality
        self.intelligence = intelligence
        self.subject = subject

        self.starting_prompt = starting_prompt.format(subject = self.subject, difficulty = self.intelligence.value)

        self.gpt_manager = ChatGPT_Manager(API_Key, starting_prompt= self.starting_prompt)
        self.tts_manager = OpenAI_TTS_Manager(API_Key, voice = random.choice(voices))
    
    def generate_question(self, message):
        #TODO MAKE THIS MORE DYNAMIC BY RANDOMISING BASED ON PERSOANLITY WETHER TO ASK OR NOT
        return self.gpt_manager.generate_response_history(message)
    
    def generate_audio(self, message):
        self.tts_manager.generate_audio(message)
        