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

git filter-branch --tree-filter "find . -type f -name '*.py' -exec sed -i 's/API_Key = \".*\"/API_Key = \"YOUR_API_KEY_HERE\"/g' {} \;" HEAD