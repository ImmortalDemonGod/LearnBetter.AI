class Chatbot:
    def __init__(self, brains, logger):
        """Constructor initializes brains and logger"""
        self.brains = brains
        self.logger = logger

    def send_message(self, message):
        """Send user message, call API, return response"""
        # Select the appropriate brain for the message
        brain = self.select_brain(message)
        # Generate the response using the selected brain
        response = brain.generate_response(message)
        return response

    def select_brain(self, message):
        """Choose the most appropriate brain for the message"""
        # For now, we'll just return the first brain in the list
        # In the future, this method should analyze the message and select the most appropriate brain
        return self.brains[0]
