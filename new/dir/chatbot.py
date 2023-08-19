from pydantic import BaseModel

class Message(BaseModel):
    content: str

class Chatbot:
    def __init__(self, brains, logger, gpt):
        """Constructor initializes brains, logger, and GPT"""
        self.brains = brains
        self.logger = logger
        self.gpt = gpt
        self.tokens_used = 0

    def send_message(self, message: Message):
        """Send user message, call API, return response"""
        # Select the appropriate brain for the message
        brain = self.select_brain(message)
        # Generate the response using the selected brain
        response = brain.generate_response(message)
        # Increment the tokens used by the number of tokens in the message and the response
        self.tokens_used += len(message.content.split()) + len(response.content.split())
        # Check if the tokens used exceed the token budget
        if self.tokens_used > 4000:
            # Summarize the conversation history and reset the tokens used
            summary = self.summarize_conversation()
            self.tokens_used = len(summary.split())
            # Send the summary to the GPT-3 model to generate the final response
            final_response = self.gpt.generate_response(summary)
        else:
            # Send the response to the GPT-3 model to generate the final response
            final_response = self.gpt.generate_response(response.content)
            # Increment the tokens used by the number of tokens used by the GPT-3 model
            self.tokens_used += len(final_response.split())
        return final_response

    def select_brain(self, message: Message):
        """Choose the most appropriate brain for the message"""
        # For now, we'll select the brain based on the content of the message
        for brain in self.brains:
            if brain.name in message.content:
                return brain
        # If no specific brain is mentioned in the message, return the first brain in the list
        return self.brains[0]

    def summarize_conversation(self):
        """Summarize the conversation history"""
        # For now, we'll return the last few messages in the conversation
        return '\n'.join(message.content for message in self.logger.get_last_messages(5))
