from flask import Flask, request, jsonify
from tasks import generate_audio_response_task
import os

os.environ["PYTHONPATH"] = f"{os.environ.get('PYTHONPATH', '')}:{os.getcwd()}"
os.environ["FLASK_APP"] = "server.py"
app = Flask(__name__)

@app.route('/generate_audio_response', methods=['POST'])
def generate_audio_response():
    data = request.get_json()
    #print("Richiesta JSON ricevuta:", data)  # Log per verificare i dati

    # Continua solo se 'audio' è presente in 'data'
    if 'audio' not in data:
        return jsonify({"error": "Campo 'audio' mancante nella richiesta"}), 400

    # Recupera i parametri dalla richiesta JSON
    audio_data = data['audio']
    subject = data['subject']
    personality = data['personality']
    intelligence = data['intelligence']
    interest = data['interest']
    happyness = data['happyness']

    # Avvia il task asincrono per generare la risposta audio
    task = generate_audio_response_task.delay(audio_data, subject, personality, intelligence, interest, happyness)
    return jsonify({"task_id": task.id}), 202


@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    result = generate_audio_response_task.AsyncResult(task_id)
    if result.ready():
        return jsonify({"status": "completed", "audio": result.result})
    else:
        return jsonify({"status": "pending"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)