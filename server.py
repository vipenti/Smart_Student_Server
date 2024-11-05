from flask import Flask, request, jsonify, Response
from celery.result import AsyncResult
import json

from tasks import create_student, generate_spoken_question, generate_written_question, test_task

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

already_started = False
can_ask_question = True


@app.route("/test", methods=["POST"])
def test():
    req = request.get_json()

    print("------TEST------")
    print(req)
    print("----------------")

    return jsonify(req)


def question_generation(task_function):
    if not already_started:
        return Response("Student not yet created!", status=400, mimetype='text/plain')

    print("[Request] Question generation requested")
    audio_data = request.get_data()

    # get the audio format from the request
    audio_format = request.headers.get('Content-Type')

    # check if the audio format is supported
    if audio_format.replace("audio/", "") not in ALLOWED_FORMATS:
        return Response("Invalid audio format", status=400, mimetype='text/plain')

    # start celery task to generate question with callback function
    task_result = task_function.delay(audio_data)

    # return the task id for the client to check the status
    return {"result_id": task_result.id}


@app.route("/generate_written_question", methods=["POST"])
def generate_question_string():
    return question_generation(generate_written_question)


@app.route("/generate_question", methods=["POST"])
def generate_question():
    return question_generation(generate_spoken_question)


@app.route("/start", methods=["POST"])
def start():
    global already_started
    already_started = True

    # get the subject from the request
    req = request.get_json()
    subject = req["subject"]


    # start the celery task to instantiate the student
    create_student.delay(subject)

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


@app.route("/test_stub", methods=["POST"])
def test_stub():
    # start celery task to return test value
    task_result = test_task.delay()

    # return the task id for the client to check the status
    return {"result_id": task_result.id}


if __name__ == "__main__":
    print("Smart Student ready on port 5000!")
    app.run(port=5000)
