import openai
from modules.textGenerationManager import TextGenerationManager


class ChatGPT_Manager(TextGenerationManager):

    # List of available models from OpenAI as of 8 March 2024
    MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview",
    ]

    def __init__(self, API_Key, model="gpt-3.5-turbo", starting_prompt=""):
        if model not in ChatGPT_Manager.MODELS:
            raise ValueError("Model not available. Available models: " +
                             ", ".join(ChatGPT_Manager.MODELS))
        
        super().__init__(API_Key, model, ({"role": "system", "content": starting_prompt}))

        openai.api_key = API_Key    # Set the API Key for OpenAI

    # Makes a regular request to OpenAI Chat API
    def generate_response_history(self, message):
        self.messages.append(
            {"role": "user", "content": message}
        )

        return self.api_call(self.messages)

    # Makes a request to OpenAI Chat API without history

    def generate_response(self, message, starting_prompt=""):
        if starting_prompt == "":
            starting_prompt = self.starting_prompt

        no_history_msgs = []

        # Add the starting prompt to the list of messages to remind the AI of the context
        no_history_msgs.append(
            {"role": "system", "content": starting_prompt}
        )

        # Add the user's message to the list of messages
        no_history_msgs.append(
            {"role": "user", "content": message}
        )

        return self.api_call(no_history_msgs)

    # Makes the actual API call to OpenAI Chat API
    def api_call(self, messages):
        reply = openai.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return reply.choices[0].message.content

    @TextGenerationManager.starting_prompt.setter
    def starting_prompt(self, value):
        
        self._starting_prompt = ({"role": "system", "content": value})
        self.messages = [self._starting_prompt]

        self.clear_history()
