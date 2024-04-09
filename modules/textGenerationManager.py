class TextGenerationManager:

    MODELS = []

    def __init__(self, API_Key, model, starting_prompt=""):
        self.API_Key = API_Key

        self.model = model  # text generation model

        # System prompt to set up the conversation
        self.starting_prompt = starting_prompt

        # List of messages exchanged in the conversation initialised with the starting prompt
        self.messages = [self.starting_prompt]

    # Makes a request saving the history of the conversation
    def generate_response_history(self, message):
        return self.api_call(message)
    
    # Makes a request without saving the history of the conversation
    def generate_response(self, message, starting_prompt=""):
        return self.api_call(message)

    # Makes the actual API call 
    def api_call(self, messages):
        pass

    # Clears the history of the conversation
    def clear_history(self):
        self.messages = []
        self.messages.append(self.starting_prompt)
