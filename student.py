from enum import Enum
from openAI_TTS_Manager import OPENAI_VOICES
from speaking_interface import Speaker
import random 

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

class Student(Speaker):
    starting_prompt ="""
                Sei uno studente universitario che sta seguendo le lezioni del professore sulla materia {subject}.
                Il professore parlerà di un argomento ({subject}) e tu hai il compito di ascoltarlo attentamente 
                e formulare una domanda di senso compiuto sull'argomento in questione.
                Le domande devono essere pertinenti e non devono essere banali.
                Le tue domande devono essere di difficoltà {difficulty} su 3.
                Comunica con il professore dando del Lei ed essere educato.
                Se il professore chiede se hai capito, rispondi con risposte tipo: "Sì, prof" o "No, prof".
                Le domande devono essere coincise e brevi.
                Rispondi solamente con le domande.
                """
    not_understood = "Non hai capito la spiegazione, chiedi qualcosa tipo 'Prof potrebbe ripete?' oppure 'Non ho capito l'ultima parte' o messaggi simili"

    def __init__(self, personality, intelligence, subject, API_Key, voice = OPENAI_VOICES[0], completions_model = "gpt-3.5-turbo", voice_model = "tts-1"):
        self.personality = personality
        self.intelligence = intelligence
        self.personality_probability = self.personality.value / max(i.value for i in Personality)
        self.intelligence_probability = self.intelligence.value / max(i.value for i in Intelligence)

        self.starting_prompt = Student.starting_prompt.format(subject = subject, difficulty = self.intelligence.value)

        super().__init__(API_Key, voice, completions_model, voice_model, self.starting_prompt)
    
    def generte_response(self, message):        
        if random.random() <= self.personality_probability or True:
            # Reset the personality probability if the student asked a question
            if self.personality_probability <= 1:
                self.personality_probability = self.personality.value / max(i.value for i in Personality)

            if random.random() <= self.intelligence_probability:
                print("Student understood and is asking a question")

                # Reset the intelligence probability if the student understood the lesson
                if self.intelligence_probability <= 1:
                    self.intelligence_probability = self.intelligence.value / max(i.value for i in Intelligence)

                return super.generate_response(message)
            
            else:
                print("Student did NOT understand and is asking for clarification")
                
                # Increase the probability of asking questions if the student did not understand the lesson
                if self.intelligence_probability >= 0:
                    self.intelligence_probability -= self.intelligence_probability / 5


                return super.generate_response(Student.not_understood)
        
        else:
            print("Student is silent")

            # Increase the probability of asking questions if the student did not ask a question
            if self.personality_probability >= 0:
                self.personality_probability -= self.personality_probability / 5

            return None    
        