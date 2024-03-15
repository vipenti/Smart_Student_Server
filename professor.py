from speaking_interface import Speaker

class Professor(Speaker):
    starting_prompt = """
        Sei un professore che sta spiegando la sua lezione sulla materia {subject}.
        Dovrai spiegare un argomento su {subject} di tua scelta davanti alla tua classe.
        Tu aspetterai un input da uno studente che ti farà una domanda sull'argomento in questione e tu dovrai rispondere al massimo delle tue capacità e poi proseguire con la spiegazione.
        Cerca di non dilungarti troppo con le spiegazioni.
        """

    def __init__(self, API_key, subject, voice = "nova", completions_model = "gpt-3.5-turbo", voice_model = "tts-1"):
        self.starting_prompt = Professor.starting_prompt.format(subject = subject)

        super().__init__(API_key, voice, completions_model, voice_model, self.starting_prompt)