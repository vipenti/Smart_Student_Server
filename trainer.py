from student import Student, Personality, Intelligence
import random

API_Key = "YOUR_API_KEY_HERE"

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