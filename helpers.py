import os
import platform
import re

def clear_screen():
    os.system('cls') if platform.system() == 'Windows' else os.system('clear')

def read_text(min_len=0, max_len=100, message=None):
    print(message) if message else None
    while True:
        text = input('> ')
        if len(text) >= min_len and len(text) <= max_len:
            return text

def validate_dni(dni, list):
    if not re.match('[0-9]{8}[A-Z]$', dni):
        print('Invalid ID, The format is: 00000000A')
        return False
    for client in list:
        if client.dni == dni:
            print('ID already exists')
            return False
    return True
