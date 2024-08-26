from enum import Enum
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
    STARTING_PROMPT = """
    Sei uno studente universitario che sta seguendo le lezioni del professore.
    Il professore parlerà dell'argomento {subject} e tu hai il compito di ascoltarlo attentamente: 
    - Quando il professore fa una domanda: devi rispondere correttamente e in poche parole
    - Quando il professore parla di un argomento: devi fare una domanda pertinente e breve
    - Quando il professore chiede se hai capito l'argomento trattato: devi rispondere con "Sì, prof" o "No, prof"
    Comunica con il professore dando del Lei ed essere educato.
    Le domande e risposte devono essere coincise e brevi."""

    NOT_UNDERSTOOD = "Non hai capito la spiegazione, chiedi qualcosa tipo 'Prof potrebbe ripete?' oppure 'Non ho capito l'ultima parte' o messaggi simili"

    UNRELATED_QUESTION = """
    Sei l'assistente del professore. Ascolterai la lezione del professore e dovrai decidere se gli studenti dovrebbero o meno fare domande.
    L'argomento della lezione di oggi è {subject}.
    Il tuo compito è specificare se per una determinata frase è pertinente fare una domanda al professore oppure no.
    Rispondi solo con True o False"""

    def __init__(self, personality, intelligence, subject, text_manager, tts_manager):
        self.personality = personality
        self.intelligence = intelligence
        self.personality_probability = self.personality.value / \
            max(i.value for i in Personality)
        self.intelligence_probability = self.intelligence.value / \
            max(i.value for i in Intelligence)

        self.subject = subject
        self.starting_prompt = Student.STARTING_PROMPT.format(
            subject=subject)

        super().__init__(text_manager, tts_manager, self.starting_prompt)

    def generate_response(self, message, check_correlation=False):
        if message is None:
            raise ValueError("Message cannot be None")

        # Check if the student should ask a question
        if check_correlation:
            is_related = self.text_manager.generate_response(
                message, self.UNRELATED_QUESTION.format(subject=self.subject))
            
            print("Is related: " + is_related)

            is_related = is_related.strip().lower()
        
        else:
            is_related = "true"

        if not check_correlation or (is_related == "true"):
            if random.random() <= self.personality_probability:
                # Reset the personality probability if the student asked a question
                if self.personality_probability <= 1:
                    self.personality_probability = self.personality.value / \
                        max(i.value for i in Personality)

                if random.random() <= self.intelligence_probability:
                    print("Student understood and is asking a question")

                    # Reset the intelligence probability if the student understood the lesson
                    if self.intelligence_probability <= 1:
                        self.intelligence_probability = self.intelligence.value / \
                            max(i.value for i in Intelligence)

                    return super().generate_response(message)

                else:
                    print("Student did NOT understand and is asking for clarification")

                    # Increase the probability of asking questions if the student did not understand the lesson
                    if self.intelligence_probability >= 0:
                        self.intelligence_probability -= self.intelligence_probability / 5

                    return super().generate_response(Student.NOT_UNDERSTOOD)

            else:
                print("Student is silent")

                # Increase the probability of asking questions if the student did not ask a question
                if self.personality_probability >= 0:
                    self.personality_probability -= self.personality_probability / 5

                return None

        elif is_related.lower() == "false":
            print("Professor speaking off-topic")

        else:
            raise ValueError("Invalid pertinence check from API call. Got: " +
                             is_related + ". Expected: True or False.")
