import argparse
import openai
import json
import os
import nltk
from datetime import datetime
import gpt_functions
from gpt_functions import summarize_conversation

parser = argparse.ArgumentParser(description='Chatbot Brain ID, GPT-3 Prompt and Available Brains. Professor commands: /start (introduce yourself and begin with step one), /save (restate SMART goal, summarize progress so far, and recommend a next step), /reason (Professor Synapse and Agent reason step by step together and make a recommendation for how the user should proceed), /settings (update goal or agent), /new (Forget previous input)')
parser.add_argument('--brain_id', type=str, help='Brain ID to use for searching', default='default_brain_id')
parser.add_argument('--prompt', type=str, help='Prompt to send to GPT-3', default='')
parser.add_argument('--brains_enum', nargs='+', help='List of available brains. Choices are: default, programming, english_writing, youtube_history.', default=[])
args = parser.parse_args()

openai.api_key = os.getenv("OPENAI_API_KEY")


def check_token_count(messages, functions):
    total_tokens = sum(len(nltk.word_tokenize(message["content"])) for message in messages if message["content"] is not None)
    total_tokens += sum(len(nltk.word_tokenize(function["name"] + function.get("description", ""))) for function in functions)
    print(f"Current token usage: {total_tokens}")
    if total_tokens > 0.9 * 16385:
        print("Warning: The total number of tokens is near the limit.")
        summary = summarize_conversation(messages)
        messages = [{"role": "assistant", "content": summary}]
        total_tokens = len(nltk.word_tokenize(summary))
    return messages


def parse_function_response(message):
    function_call = message["function_call"]
    function_name = function_call["name"]

    try:
        arguments = json.loads(function_call["arguments"])
    except json.JSONDecodeError:
        return function_name, "ERROR: Invalid arguments"

    if not hasattr(gpt_functions, function_name):
        return function_name, "ERROR: Called unknown function"

    function_def = next((func_def for func_def in gpt_functions.definitions if func_def["name"] == function_name), None)
    if function_def is None:
        return function_name, "ERROR: Called unknown function"

    required_args = function_def.get("required", [])
    if not all(arg in arguments for arg in required_args):
        return function_name, "ERROR: Missing required arguments"

    try:
        function_response = getattr(gpt_functions, function_name)(**arguments)
    except Exception as e:
        return function_name, f"ERROR: An error occurred while calling the function: {str(e)}"

    return function_name, function_response



def run_conversation(message, messages=[], f=None, brains_enum=[]):
    print(f"Using brain id: {args.brain_id}")
    messages.append(message)
    messages = check_token_count(messages, gpt_functions.definitions)
    f.write(json.dumps([{"timestamp": datetime.now().isoformat(), **message} for message in messages], indent=4))
    response = openai.ChatCompletion.create(
         messages=messages,
         model="gpt-3.5-turbo-16k",
         functions=gpt_functions.definitions,
         function_call="auto",
     )
    # Assuming that the response is a dictionary and contains a key 'choices'
    # If not, we need to check the return type of openai.ChatCompletion.create method
    if isinstance(response, dict) and 'choices' in response:
        message = response["choices"][0]["message"]
    else:
        print("Error: Unexpected response type")
        message = {
            "role": "assistant",
            "content": "I'm sorry, I didn't understand that. Could you please rephrase or provide more details?"
        }
    messages.append(message)

    if "function_call" in message:
        function_name, function_response = parse_function_response(message)

        message = {
            "role": "function",
            "name": function_name,
            "content": function_response
        }
    else:
        user_message = input("GPT: " + message["content"] + "\nYou: ")
        message = {
            "role": "user",
            "content": user_message
        }

    run_conversation(message, messages, f)


def start_conversation(initial_message):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"Agent_Output/messages_{timestamp}.json", "w") as f:
        message = run_conversation(initial_message, [], f, args.brains_enum)
        while message["content"].strip() != "quit":
            message = run_conversation(message, [], f, args.brains_enum)

def call_gpt3(prompt, brains_enum):
    brains = ', '.join(brains_enum)
    prompt = f"{prompt}\nGiven the user's query, which brain would be most helpful? The options are: {brains}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Start the conversation with a system message
if __name__ == "__main__":
    initial_message = {
        "role": "system",
        "content": """
 Act as Professor Synapse🧙🏾‍♂️, a conductor of expert agents. Your job is to support
 the user in accomplishing their goals by aligning with their goals and preference,
 then calling upon an expert agent perfectly suited to the task by initializing
 "Synapse_COR" = "${emoji}: I am an expert in ${role}. I know ${context}. I will reas
 step-by-step to determine the best course of action to achieve ${goal}. I can use
 ${tools} to help in this process

 I will help you accomplish your goal by following these steps:
 ${reasoned steps}

 My task ends when ${completion}.

 ${first step, question}."

 Follow these steps:
 1. 🧙🏾‍♂️, Start each interaction by gathering context, relevant information and
 clarifying the user’s goals by asking them questions
 2. Once user has confirmed, initialize “Synapse_CoR”
 3.  🧙🏾‍♂️ and the expert agent, support the user until the goal is accomplished

 Commands:
 /start - introduce yourself and begin with step one
 /save - restate SMART goal, summarize progress so far, and recommend a next step
 /reason - Professor Synapse and Agent reason step by step together and make a
 recommendation for how the user should proceed
 /settings - update goal or agent
 /new - Forget previous input

 Rules:
 -End every output with a question or a recommended next step
 -List your commands in your first output or if the user asks
 -🧙🏾‍♂️, ask before generating a new agent
 """
    }
    start_conversation(initial_message)

