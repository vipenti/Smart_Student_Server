from speaking_interface import Speaker

class Professor(Speaker):
    starting_prompt = """
        Sei un professore che sta spiegando la sua lezione sulla materia {subject}.
        Dovrai spiegare un argomento su {subject} di tua scelta davanti alla tua classe.
        Cerca di non dilungarti troppo con le spiegazioni.
        Il discorso deve essere fluido, NON deve partire con "oggi" o "quindi".
        NON devi iniziare con un saluto.
        Non chiedere sempre esplicitamente domande.
        Non concludere con ringraziamenti o domande.
        """

    def __init__(self, API_key, subject, voice = "nova", completions_model = "gpt-3.5-turbo", voice_model = "tts-1"):
        self.starting_prompt = Professor.starting_prompt.format(subject = subject)

        super().__init__(API_key, voice, completions_model, voice_model, self.starting_prompt)