#!/Users/pedrorico/.pyenv/versions/comai/bin/python

import openai
import os
import sys
# import bcolors
from colorama import Fore
from termcolor import colored
from dotenv import load_dotenv
from getch import getch

load_dotenv()

# Authenticate with the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

assert len(sys.argv) > 1

input_text = ' '.join(sys.argv[1:])

prompt = (f"Convert the following natural language instruction to a Unix command:\n"
            f"{input_text}\n"
            f"UNIX command:")

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=60,
    n=1,
    stop=None,
    temperature=0.2,
)

command = response.choices[0].text.strip()
# command = 'ls'

# print('>>> ' + colored(command, 'cyan'), end='')
# confirmation = input()
# if confirmation == '':
#     os.system(command)

output = '>>> ' + colored(command, 'cyan') #+ colored(" ['Enter' to validate, other key to cancel]", 'black')
print(output, end='', flush=True)

char = getch()
if char == "\n":
    print()
    os.system(command)
# elif char == "\x1b":
#     exit()
