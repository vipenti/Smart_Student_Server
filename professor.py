from speaking_interface import Speaker

class Professor(Speaker):
    STARTING_PROMPT = """
        Sei un professore che sta spiegando la sua lezione sulla materia {subject}.
        Dovrai spiegare un argomento su {subject} di tua scelta davanti alla tua classe.
        Cerca di non dilungarti troppo con le spiegazioni.
        Il discorso deve essere fluido, NON deve partire con "oggi" o "quindi".
        NON devi iniziare con un saluto.
        Non chiedere sempre esplicitamente domande.
        Non concludere con ringraziamenti o domande.
        """

    def __init__(self, subject):
        # Crea il prompt di partenza per il professore
        self.starting_prompt = Professor.STARTING_PROMPT.format(subject=subject)

        # Inizializza la classe `Speaker` con il prompt di partenza
        super().__init__(self.starting_prompt)
