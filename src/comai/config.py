import os
import pickle
import configparser
import typer
from typing import List
from cryptography.fernet import Fernet
from .interactions import Interaction

CONTEXT_SIZE = 20
APP_NAME = "comai"
config_dir = typer.get_app_dir(APP_NAME, force_posix=True)
key_path = os.path.join(config_dir, "config.ini")
session_id = os.getenv('COMAI_SESSION')
log_path = None
try:
    log_path = os.path.join(config_dir, session_id)
except Exception:
    pass

encryption_key = b'QUMSqTJ5nape3p8joqkgHFCzyJdyQtqzHk6dCuGl9Nw='
cipher_suite = Fernet(encryption_key)

def save_api_key(api_key):
    encrypted_key = cipher_suite.encrypt(api_key.encode())
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"api_key": encrypted_key.decode()}

    os.makedirs(config_dir, mode=0o700,  exist_ok=True)
    def opener(path, flags):
        return os.open(path, flags, 0o600)
    with open(key_path, "w", opener=opener) as configfile:
        config.write(configfile)

def load_api_key():
    try:
        config = configparser.ConfigParser()
        config.read(key_path)
        encrypted_key = config["DEFAULT"]["api_key"].encode()
        decrypted_key = cipher_suite.decrypt(encrypted_key)
        return decrypted_key.decode()
    except Exception:
        return None

def delete_api_key():
    if os.path.isfile(key_path):
        os.remove(key_path)

def save_interaction(interaction: Interaction):
    if log_path:
        interactions = get_prev_interactions()
        interactions.append(interaction)
        if len(interactions) > CONTEXT_SIZE:
            interactions = interactions[-CONTEXT_SIZE:]
        with open(log_path, 'bw') as log_file:
            pickle.dump(interactions, log_file)

def get_prev_interactions() -> List[Interaction]:
    try:
        with open(log_path, 'br') as log_file:
            return pickle.load(log_file)
    except Exception:
        return []
