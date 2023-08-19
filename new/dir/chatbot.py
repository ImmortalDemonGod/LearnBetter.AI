from pydantic import BaseModel

class Message(BaseModel):
    content: str

class Chatbot:
    def __init__(self, brains, logger, gpt):
        """Constructor initializes brains, logger, and GPT"""
        self.brains = brains
        self.logger = logger
        self.gpt = gpt

    def send_message(self, message: Message):
        """Send user message, call API, return response"""
        # Select the appropriate brain for the message
        brain = self.select_brain(message)
        # Generate the response using the selected brain
        response = brain.generate_response(message)
        # Send the response to the GPT-3 model to generate the final response
        final_response = self.gpt.generate_response(response.content)
        return final_response

    def select_brain(self, message: Message):
        """Choose the most appropriate brain for the message"""
        # For now, we'll just return the first brain in the list
        # In the future, this method should analyze the message and select the most appropriate brain
        return self.brains[0]
