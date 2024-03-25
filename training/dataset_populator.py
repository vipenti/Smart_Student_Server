from modules.chatGPT_Manager import ChatGPT_Manager
from professor import Professor
import random
import json
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Populate the dataset with random conversations of a professor and a random guy')
parser.add_argument('max_iterations', type=int, help='The maximum number of iterations to run the script for')

max_iterations = parser.parse_args().max_iterations

with open('configs/API_key.json') as config_file:
    data = json.load(config_file)

# OpenAI API key
API_Key = data['API_KEY']


with open('configs/subjects.json') as subjects_file:
    subjects = json.load(subjects_file)

guy_starting_prompt = """Stai raccontando ai tuoi studenti un aneddoto a caso OPPURE una storiella che non è inerente alla lezione. 
Non raccontare aneddoti o storie troppo lunghe. 
Non devi iniziare annunciando il fatto che stai per raccontare.
Non devi iniziare con "casuale" o "casualmente".
Non devi iniziare con un saluto.
Non devi introdurre il discorso.
Non terminare con frasi che indicano un ritorno al discorso."""

professor_response_list = []
guy_response_list = []

saving_percent = max_iterations // 10
saving_percent = 1 if saving_percent <= 1 else saving_percent

for i in range(max_iterations):
    # Randomly select a subject, random key, random element of array
    random_subject = random.choice(subjects[random.choice(list(subjects.keys()))])

    print(f"\rRunning #{i+1} iteration <Subject: {random_subject}>", end="")

    professor = Professor(API_Key, random_subject, completions_model=ChatGPT_Manager.MODELS[1])
    random_guy = ChatGPT_Manager(API_Key, starting_prompt= guy_starting_prompt, model=ChatGPT_Manager.MODELS[1])

    # Generate responses from both
    guy_response = random_guy.generate_response_history("genera").replace("\"", "'")
    professor_response = professor.generate_response("partiamo").replace("\"", "'")

    guy_response = guy_response.replace("\n", " ")
    professor_response = professor_response.replace("\n", " ")

    # print(f"Professor: {professor_response}")
    # print(f"Random guy: {guy_response}")

    # Append to the lists
    professor_response_list.append(professor_response)
    guy_response_list.append(guy_response)

    if (i+1) % saving_percent == 0 or i+1 == max_iterations:
        print(f" [Saved]")

        # Turn them into dataframes 
        prof_df = pd.DataFrame({
            "text": professor_response_list,
            "speaker": "'professor'"
        })

        guy_df = pd.DataFrame({
            "text": guy_response_list,
            "speaker": "'random_guy'"
        })

        # Convert to csv or parquet    
        prof_df.to_csv("data/professor.csv", mode='a', header=False, index=False)
        guy_df.to_csv("data/random_guy.csv", mode='a', header=False, index=False)

        professor_response_list = []
        guy_response_list = []