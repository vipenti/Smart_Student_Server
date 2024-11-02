import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disabilita il parallelismo per evitare deadlock

from student import Student, Personality, Intelligence, Interest, Happyness
from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import torch
import requests
import json

class StudentTest:
    def __init__(self, subject, personality=None, intelligence=None, interest=None, happyness=None):
        # Carica il modello di testo Hugging Face
        print("Caricamento del modello di Hugging Face...")
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")  # oppure "distilgpt2"
        self.model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

        
        # Crea uno studente con caratteristiche specificate o casuali
        self.student = Student(
            subject=subject,
            personality=personality if personality else random.choice(list(Personality)),
            intelligence=intelligence if intelligence else random.choice(list(Intelligence)),
            interest=interest if interest else random.choice(list(Interest)),
            happyness=happyness if happyness else random.choice(list(Happyness))
        )
        
        print(f"Studente creato per l'argomento: {subject}")
        print(f"Caratteristiche: Personalità={self.student.personality.name}, Intelligenza={self.student.intelligence.name}, "
              f"Interesse={self.student.interest.name}, Felicità={self.student.happyness.name}")
    
    def pass_transcription(self, transcription):
        print("\n[Professore] Trascrizione del discorso:")
        print(transcription)
        
        # Costruisci un prompt più semplice
        prompt_completo = (
            "Sei uno studente che sta seguendo una lezione su un argomento specifico.\n"
            "Ascolta attentamente e rispondi brevemente o fai una domanda pertinente in base al discorso del professore.\n\n"
            "[Discorso del docente:]\n"
            f"{transcription}\n\n"
            "[Risposta dello studente]:"
        )
        
        # Tokenizza e stampa il prompt completo che viene passato al modello
        inputs = self.tokenizer(prompt_completo, return_tensors="pt")
        print("\n[Debug] Prompt completo passato al modello (decodificato):")
        print(self.tokenizer.decode(inputs.input_ids[0]))

        # Genera l'output del modello
        outputs = self.model.generate(
            inputs.input_ids, 
            max_new_tokens=50,  # Limita il numero di nuovi token per evitare risposte troppo lunghe
            attention_mask=inputs.attention_mask,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50
        )
        generated_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Stampa la risposta generata senza il prompt
        risposta = generated_response.replace("Ciao, come stai oggi?", "").strip()
        print("\n[Studente] Risposta generata:")
        print(risposta)

def api_call():
    subject = "How to cook a pizza margherita"
    transcription = """Making a homemade pizza starts with the dough base.
        To make it, we need a few essential ingredients: flour, water, yeast, salt and
        a drizzle of olive oil. We start by dissolving the yeast in a little warm water, which activates
        the yeast and helps the dough rise. While the yeast dissolves, we can arrange the flour
        in a fountain shape on a clean work surface or directly in a large bowl."""
    
    test = Student(
        subject,
        personality=Personality.OUTGOING,
        intelligence=Intelligence.LOW,
        interest=Interest.UNINTERESTED,
        happyness=Happyness.SAD
    )

    student_prompt = test.starting_prompt
    professor_prompt = "\n[Professor speech start:]" + transcription + " [Professor speech end]"
    print(student_prompt)

    message = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [ 
            { "role": "system", "content": student_prompt},
            { "role": "user", "content": professor_prompt}
    ], 
    "temperature": 0.7, 
    "max_tokens": -1
    }

    response = requests.post(url="http://192.168.4.53:1234/v1/chat/completions",json=message)

    print(response)

# Esempio di utilizzo della classe di test
if __name__ == "__main__":

    api_call()
    
def monnezza():
    subject = "La pizza margherita"
    transcription = """La preparazione di una pizza fatta in casa inizia con la base dell'impasto. 
    Per prepararlo, abbiamo bisogno di pochi ingredienti essenziali: farina, acqua, lievito, sale e 
    un filo d'olio d'oliva. Si comincia sciogliendo il lievito in un po' di acqua tiepida, che attiva 
    il lievito e aiuta l'impasto a lievitare. Mentre il lievito si scioglie, possiamo disporre la farina
     a fontana su una superficie di lavoro pulita o direttamente in una ciotola capiente."""

    # Inizializza il test con un argomento e caratteristiche specifiche dello studente
    test = StudentTest(
        subject,
        personality=Personality.OUTGOING,
        intelligence=Intelligence.HIGH,
        interest=Interest.VERY_INTERESTED,
        happyness=Happyness.HAPPY
    )

    # Passa una trascrizione e genera la risposta
    test.pass_transcription("transcription")