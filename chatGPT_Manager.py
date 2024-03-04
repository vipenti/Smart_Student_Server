import openai

class ChatGPT_Manager:
    def __init__(self, API_Key, model="gpt-3.5-turbo", starting_prompt = ""):
        self.API_Key = API_Key
        self.model = model
        self.starting_prompt = ({"role": "system", "content": starting_prompt})
        self.messages = [self.starting_prompt]

        openai.api_key = API_Key
        
    # Makes a regular request to OpenAI Chat API  
    def generate_response_history(self, message):
        self.messages.append(
                {"role": "user", "content": message}
            )
        
        return self.api_call(self.messages)

        
    # Makes a request to OpenAI Chat API without history
    def generate_response(self, message, starting_prompt = ""):

        no_history_msgs = []

        no_history_msgs.append(
            {"role": "system", "content": starting_prompt}
        )
        
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
    
    def clear_history(self):
        self.messages = []

