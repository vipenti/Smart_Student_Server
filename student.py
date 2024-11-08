from enum import Enum
import random
import requests
import re


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


def clean_answer(answer):
    cleaned_answer = re.sub(r'\[.*?\]|\*.*?\*', '', answer)
    return ' '.join(cleaned_answer.split())


class Student:
    STARTING_PROMPT = """Act as if you were a student attending a professor's lecture. Impersonate a student with the 
    following characteristics, which describe four parameters of the student's personality: 
    - Extroverted: {personality} 
    - Intelligence: {intelligence} 
    - Interested in the lecture: {interest} 
    - Happy: {happyness} 

    You will listen to the professor's presentation, whose main topic will be: {subject}. You have the task of behaving like a 
    realistic student, more specifically you can: 
    - Answer a question posed by the professor. The answer must be short and concise, as if a student were answering. 
    - Ask questions to the professor. The question you ask must be about the presentation you are listening to and can be 
      (1) a request for clarification, (2) a question for further information, (3) asking to repeat a part that you think 
      was not clear. 

    Impersonate the student following the parameters of your personality. The answer must report only and exclusively 
    the student's words. Provide only the student's vocal response, absolutely avoiding any description of actions or 
    thoughts, such as "*looks down*", "[laughs]", etc. Spoken words only."""

    def __init__(self, subject, personality, intelligence, interest, happyness):
        # Assegna i valori passati o genera casualmente
        self.personality = personality if personality is not None else random.choice(list(Personality))
        self.intelligence = intelligence if intelligence is not None else random.choice(list(Intelligence))
        self.interest = interest if interest is not None else random.choice(list(Interest))
        self.happyness = happyness if happyness is not None else random.choice(list(Happyness))

        self.subject = subject
        self.starting_prompt = Student.STARTING_PROMPT.format(
            subject=subject,
            personality=self.personality.name,
            intelligence=self.intelligence.name,
            interest=self.interest.name,
            happyness=self.happyness.name
        )

    def generate_response(self, transcription):
        student_prompt = self.starting_prompt
        professor_prompt = "\n[Professor speech start:]" + transcription + " [Professor speech end]"
        message = {
            "model": "meta-llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": student_prompt},
                {"role": "user", "content": professor_prompt}
            ],
            "temperature": 0.9,
            "max_tokens": -1
        }

        response = requests.post(url="http://25.53.69.231:1234/v1/chat/completions", json=message)
        response_data = response.json()

        content_message = clean_answer(response_data["choices"][0]["message"]["content"])
        print(content_message)
        return content_message

