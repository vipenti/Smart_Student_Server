import base64
from flask import Flask, request, jsonify, Response
from student import Student, Personality, Intelligence
from celery.result import AsyncResult
import random
import json
import whisper

from modules.openAI_TTS_Manager import OpenAI_TTS_Manager
from modules.chatGPT_Manager import ChatGPT_Manager
from tasks import create_student, generate_spoken_question

ALLOWED_FORMATS = [
    "m4a",
    "mp3",
    "webm",
    "mp4",
    "mpga",
    "wav",
    "mpeg",
]

app = Flask(__name__)

# student = None
# model = None
already_started = False
can_ask_question = True
OpenAI_Key = None
ElevLabs_Key = None

with app.app_context():
    # print("Loading the model.")
    # model = whisper.load_model("small")

    with open('configs/API_key.json') as config_file:
        data = json.load(config_file)

    # OpenAI API key
    OpenAI_Key = data['OpenAI']
    ElevLabs_Key = data['ElevenLabs']

@app.route("/test", methods=["POST"])
def test():
    req = request.get_json()

    print("------TEST------")
    print(req)
    print("----------------")

    return jsonify(req)

@app.route("/generate_question", methods=["POST"])
def generate_question():
        # if student is not created, return an error
        if not already_started:
            return Response("Studente non ancora creato!", status=400, mimetype='text/plain')
        
        # get the audio data from the request
        print("[Request] Question generation requested")
        audio_data = request.get_data()

        # get the audio format from the request
        audio_format = request.headers.get('Content-Type')

        # check if the audio format is supported
        if audio_format.replace("audio/", "") not in ALLOWED_FORMATS:
            return jsonify({"error": "Formato audio non supportato"})

        # start celery task to generate spoken question
        task_result = generate_spoken_question.delay(audio_data)

        # return the task id for the client to check the status
        return {"result_id": task_result.id}

@app.route("/start", methods=["POST"])
def start():
    global already_started
    already_started = True

    # get the subject from the request
    req = request.get_json()
    subject = req["subject"]

    # start the celery task to instantiate the student
    create_student.delay(subject, OpenAI_Key)
    
    return jsonify({"message": "Studente creato con successo"})

@app.route("/result/<id>", methods=["POST"])
def task_result(id: str) -> dict[str, object]:
    # get the task result from its id
    task_result = AsyncResult(id)

    # return task ready status, successful status, and value if ready
    return jsonify({
        "ready": task_result.ready(),
        "successful": task_result.successful(),
        "value": task_result.result if task_result.ready() else None,
    })

if __name__ == "__main__":
    print("Smart student pronto all'uso\n[In ascolto sulla porta 5000]")
    app.run(port = 5000)
            