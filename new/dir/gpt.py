class GPT:
    def __init__(self, api_key):
        """Constructor initializes api_key"""
        self.api_key = api_key

    def generate_response(self, message):
        """Generate a text response to the message"""
        # For now, we'll just return a hardcoded response
        # In the future, this method should call the GPT-3 API and return the generated response
        return "Hello, I'm your chatbot!"
