from pydantic import BaseModel

class Message(BaseModel):
    content: str

class Brain:
    def __init__(self, name, personality):
        """Constructor initializes state"""
        self.name = name
        self.personality = personality

    def generate_response(self, message: Message):
        """Generate a response to the given message"""
        # For now, we'll just return a hardcoded response
        # In the future, this method should generate a response based on the brain's personality and the message content
        return Message(content="Hello, I'm your brain!")

    def get_name(self):
        """Get the name of the brain"""
        # Return the name of the brain
        return self.name
