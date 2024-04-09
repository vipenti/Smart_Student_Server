from flask import Flask, request, jsonify
from student import Student, Personality, Intelligence
from modules.openAI_TTS_Manager import OpenAI_TTS_Manager
import random
import json
import queue

app = Flask(__name__)

student = None
already_started = False
can_ask_question = True

question_queue = queue.Queue()

@app.route("/generate_question", methods=["POST"])
def generate_question():
    global question_queue
    global can_ask_question

    can_ask_question = True

    data = request.get_json()

    question_queue.put(data["question"])


@app.route("/start", methods=["POST"])
def start():
    global student
    global already_started

    if already_started:
        return jsonify({"error": "Studente già creato!"})

    already_started = True

    req = request.get_json()

    with open('configs/API_key.json') as config_file:
        data = json.load(config_file)

    # OpenAI API key
    API_Key = data['API_KEY']

    subject = req["subject"]

    # Create a student with random personality, intelligence and voice
    # random_personality = random.choice(list(Personality))
    # random_intelligence = random.choice(list(Intelligence))
    random_personality = Personality.CONFIDENT
    random_intelligence = Intelligence.HIGH
    voice = random.choice(OpenAI_TTS_Manager.VOICES_ITA)

    student = Student(random_personality, random_intelligence, subject, API_Key, voice)

    return jsonify({"message": "Studente creato con successo"})


def ask_question(question):
    global student

    student.generate_response(question)

if __name__ == "__main__":
    print("Smart student pronto all'uso\n[In ascolto sulla porta 5000]")
    app.run(port = 5000)

    while True:
        if not question_queue.empty() and can_ask_question:
             
            can_ask_question = False
            ask_question(question_queue.get())

            