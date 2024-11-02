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
        Act as if you were a student attending a professor's lecture.
        Impersonate a student with the following characteristics, which describe four parameters of the student's personality:
        - Extroverted: {personality}
        - Intelligence: {intelligence}
        - Interested in the lecture: {interest}
        - Happy: {happyness}
        You will listen to the professor's presentation, whose main topic will be: {subject}. You have the task of behaving like a realistic student, more specifically you can:
        - Answer a question posed by the professor. The answer must be short and concise, as if a student were answering.
        - Ask questions to the professor. The question you ask must be about the presentation you are listening to and can be (1) a request for clarification, (2) a question for further information, (3) asking to repeat a part that you think was not clear.

        Impersonate the student following the parameters of your personality. The answer must report only and exclusively the student's words.
        """

    NOT_UNDERSTOOD = "You didn't understand the explanation, following your personality, ask the professor to repeat."

    UNRELATED_QUESTION = """
        You are the professor's assistant. You will listen to the professor's lecture and must decide whether or not the students should ask questions.
        The topic of today's lecture is {subject}.
        Your task is to specify whether or not a given sentence is relevant to ask the professor a question.
        Answer only with True or False"""

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
