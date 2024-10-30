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
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5

class Interest(Enum):
    UNINTERESTED = 1
    SLIGHTLY_INTERESTED = 2
    NEUTRAL = 3
    INTERESTED = 4
    VERY_INTERESTED = 5

class Happyness(Enum):
    SAD = 1
    UNHAPPY = 2
    NEUTRAL = 3
    HAPPY = 4
    VERY_HAPPY = 5

class Student(Speaker):
    STARTING_PROMPT = """
    Agisci come se fossi uno studente che sta assistendo a una lezione di un professore.
    Impersona uno studente con queste caratteristiche, che vanno su una scala da 1 a 5:
    - Estroverso: {personality}
    - Intelligente: {intelligence}
    - Interessato alla lezione: {interest}
    - Felice: {happyness}
    Ascolterai la presentazione del professore, il cui argomento principale riguarderà {subject}. Hai il compito di comportarti come
    uno studente realistico, più nello specifico potrai:
    - Rispondere a una domanda posta dal professore. La risposta deve essere breve e concisa, come se stesse rispondendo uno studente.
    - Fare domande al professore. La domanda che fai deve riguardare la presentazione che stai ascoltando e può essere (1) la richiesta
    di un chiarimento, (2) una domanda di approfondimento, (3) chiedere di ripetere una parte che secondo te non è stata chiara.

    Comunica con il professore dando del Lei e seguendo i parametri della tua personalità.
    """

    NOT_UNDERSTOOD = "Non hai capito la spiegazione, seguendo la tua personalità, chiedi al professore di ripetere."

    UNRELATED_QUESTION = """
    Sei l'assistente del professore. Ascolterai la lezione del professore e dovrai decidere se gli studenti dovrebbero o meno fare domande.
    L'argomento della lezione di oggi è {subject}.
    Il tuo compito è specificare se per una determinata frase è pertinente fare una domanda al professore oppure no.
    Rispondi solo con True o False"""

    def __init__(self, subject, personality=None, intelligence=None, interest=None, happyness=None):
        # Assegna i valori passati o genera casualmente
        self.personality = personality if personality is not None else random.choice(list(Personality))
        self.intelligence = intelligence if intelligence is not None else random.choice(list(Intelligence))
        self.interest = interest if interest is not None else random.choice(list(Interest))
        self.happyness = happyness if happyness is not None else random.choice(list(Happyness))

        # Calcola le probabilità basate sui valori di personalità e intelligenza
        self.personality_probability = self.personality.value / max(i.value for i in Personality)
        self.intelligence_probability = self.intelligence.value / max(i.value for i in Intelligence)

        self.subject = subject
        self.starting_prompt = Student.STARTING_PROMPT.format(
            subject=subject,
            personality=self.personality.name,
            intelligence=self.intelligence.name,
            interest=self.interest.name,
            happyness=self.happyness.name
        )

        # Inizializza la classe genitore `Speaker` con il prompt di partenza
        super().__init__(self.starting_prompt)

    def generate_response(self, message, check_correlation=False):
        if message is None:
            raise ValueError("Message cannot be None")

        # Check if the student should ask a question
        if check_correlation:
            is_related = self.text_manager.generate_response(message, self.UNRELATED_QUESTION.format(subject=self.subject))
            print("Is related: " + is_related)
            is_related = is_related.strip().lower()
        else:
            is_related = "true"

        if not check_correlation or (is_related == "true"):
            if random.random() <= self.personality_probability:
                if self.personality_probability <= 1:
                    self.personality_probability = self.personality.value / max(i.value for i in Personality)

                if random.random() <= self.intelligence_probability:
                    print("Student understood and is asking a question")
                    if self.intelligence_probability <= 1:
                        self.intelligence_probability = self.intelligence.value / max(i.value for i in Intelligence)

                    return super().generate_response(message)
                else:
                    print("Student did NOT understand and is asking for clarification")
                    if self.intelligence_probability >= 0:
                        self.intelligence_probability -= self.intelligence_probability / 5

                    return super().generate_response(Student.NOT_UNDERSTOOD)
            else:
                print("Student is silent")
                if self.personality_probability >= 0:
                    self.personality_probability -= self.personality_probability / 5

                return None
        elif is_related.lower() == "false":
            print("Professor speaking off-topic")
        else:
            raise ValueError("Invalid pertinence check from API call. Got: " + is_related + ". Expected: True or False.")
