import openai

class ChatGPT_Manager:
    def __init__(self, API_Key, model="gpt-3.5-turbo", starting_prompt = None):
        self.API_Key = API_Key
        self.model = model
        self.messages = []
        openai.api_key = API_Key
        if starting_prompt:
            self.messages.append({"role": "system", "content": starting_prompt})

    # Makes a regular request to OpenAI Chat API  
    def generate_response_history(self, message):
        self.messages.append(
                {"role": "user", "content": message}
            )
        
        return self.api_call(self.messages)

        
    # Makes a request to OpenAI Chat API without history
    def generate_response(self, message):

        no_history_msgs = []

        no_history_msgs.append({"role": "system", "content": "You are a student."})
        no_history_msgs.append(
            {"role": "user", "content": message}
        )

        return self.api_call(no_history_msgs)

    # Makes the actual API call to OpenAI Chat API
    def api_call(self, messages):
        reply = openai.chat.completions.create(
            model = self.model,

            messages = messages
        )

        return reply.choices[0].message.content