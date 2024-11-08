from student import Student, Personality, Intelligence, Interest, Happyness
from tasks import generate_audio_response_task
import os
import requests
import base64
import time

def test_generate_audio_response(server_url, audio_file_path):

    with open(audio_file_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

    request_data = {
        "audio": audio_data,
        "subject": "3D Modeling",  # Esempio di soggetto
        "personality": 5,
        "intelligence": 1,
        "interest": 1,
        "happyness": 1
    }

    response = requests.post(f"{server_url}/generate_audio_response", json=request_data)

    # Controlla se la richiesta ha avuto successo
    if response.status_code == 202:
        print("Richiesta inviata con successo!")
        response_json = response.json()
        print("Risposta JSON:", response_json)
        return response_json
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        print(response.text)
        return None



def api_call():
    subject = "3D Modeling"
    transcription = """3D modeling is the process of creating three-dimensional representations of objects using 
    specialized software. This process begins with defining the basic geometry of the object, often starting with 
    simple shapes such as cubes, spheres, or planes. These basic shapes are then modified through operations such 
    as extruding, scaling, and rotating to achieve the desired shape.

    Next, the model is refined by adding more complex details, such as curves, irregular surfaces, and small features. 
    During this phase, modelers work with polygons and vertices, adjusting specific points to achieve a more precise  
    and realistic structure.

    Once the geometry is complete, the next step is UV mapping, a process that flattens the surface of the model to
     allow for the application of two-dimensional textures. These textures add visual details such as colors,
      materials, and fine details (for example, wood or metal).

    Finally, to give realism to the model, materials and lights are applied. Materials determine the properties
     of the object, such as reflectivity, opacity, and roughness, while lights simulate the light sources that 
     illuminate the model in the scene."""

    test = Student(
        subject,
        personality=Personality.SHY,
        intelligence=Intelligence.LOW,
        interest=Interest.UNINTERESTED,
        happyness=Happyness.SAD
    )

    print(test.generate_response(transcription))

def celery_test():

    input_file = os.path.join(os.path.dirname(__file__), "sounds/test.wav")

    with open(input_file, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

    generate_audio_response_task(audio_base64, "3D Modeling", Personality.SHY, Intelligence.LOW, Interest.UNINTERESTED, Happyness.SAD)


if __name__ == "__main__":
    # Esegui il test con l'URL del server e il percorso del file audio
    server_url = "http://127.0.0.1:5000"  # Cambia se il server è in esecuzione su un altro host o porta
    input_file = os.path.join(os.path.dirname(__file__), "sounds/test.wav")

    # Test della funzione
    response = test_generate_audio_response(server_url, input_file)

    # Se la risposta contiene un task_id, verifica lo stato del task
    if response and "task_id" in response:
        task_id = response["task_id"]
        for _ in range(10):  # Prova fino a 5 volte
            result_response = requests.get(f"{server_url}/result/{task_id}")

            if result_response.status_code == 200:
                try:
                    result_json = result_response.json()
                    print("Risultato del task:", result_json)
                    break  # Esce dal ciclo se il risultato è disponibile e in formato JSON
                except ValueError:
                    print("La risposta non è in formato JSON. Contenuto:", result_response.text)
            else:
                print(f"Task in sospeso, stato HTTP: {result_response.status_code}. Ritentando...")

            # Aspetta qualche secondo prima di riprovare
            time.sleep(2)
        else:
            print("Il task non è stato completato entro il tempo limite.")
