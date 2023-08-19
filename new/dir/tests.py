import unittest
from unittest.mock import patch
from new.dir.chatbot import Chatbot
from new.dir.brains import Brain

class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = Chatbot()

    @patch.object(Brain, 'generate_response', return_value='Hello, world!')
    def test_send_message(self):
        message = 'Hello'
        response = self.chatbot.send_message(message)
        self.assertEqual(response, 'Hello, world!')

if __name__ == '__main__':
    unittest.main()
