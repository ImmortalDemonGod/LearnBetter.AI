import argparse
from chatbot import Chatbot
from gpt import GPT
from brains import Brain
from logger import Logger

def main():
    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument('--message', type=str, help='Message to send to the chatbot')
    args = parser.parse_args()

    # Initialize the brains
    brains = [Brain('Brain1', 'Personality1'), Brain('Brain2', 'Personality2')]

    # Initialize the logger
    logger = Logger()

    # Initialize the GPT-3 wrapper
    gpt = GPT('api_key')

    # Initialize the chatbot
    chatbot = Chatbot(brains, logger, gpt)

    # Send the message to the chatbot and print the response
    response = chatbot.send_message(args.message)
    print(response)

if __name__ == '__main__':
    main()
