from student import Student, Personality, Intelligence
import random
import json

with open('configs/API_key.json') as config_file:
    data = json.load(config_file)

# OpenAI API key
API_Key = data['API_KEY']

subject = [
    "Matematica",
    "Fisica",
    "Chimica",
    "Biologia",
    "Informatica",
    "Storia",
    "Filosofia",
    "Letteratura",
    "Arte",
    "Economia",
    "Geografia",
    "Inglese",
    "Francese",
    "Italiano",
    "Scienze motorie",
    "Religione",
    "Educazione civica",
    "Musica"
]

student = Student(Personality.CONFIDENT, Intelligence.HIGH, random.choice(subject), API_Key)