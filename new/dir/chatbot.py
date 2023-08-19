class Chatbot:
    def __init__(self, brains, logger):
        """Constructor initializes brains and logger"""
        self.brains = brains
        self.logger = logger

    def send_message(self, message):
        """Send user message, call API, return response"""
        pass

    def select_brain(self, message):
        """Choose the most appropriate brain for the message"""
        pass
