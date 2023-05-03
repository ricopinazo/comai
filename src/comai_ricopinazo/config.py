import configparser
import os
import appdirs
from cryptography.fernet import Fernet

app_name = "comai"
app_author = "ricopinazo"
config_dir = appdirs.user_config_dir(app_name, app_author)
os.makedirs(config_dir, exist_ok=True)
config_path = os.path.join(config_dir, "config.ini")

encryption_key = b'QUMSqTJ5nape3p8joqkgHFCzyJdyQtqzHk6dCuGl9Nw='
cipher_suite = Fernet(encryption_key)

def save_api_key(api_key):
    encrypted_key = cipher_suite.encrypt(api_key.encode())
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"api_key": encrypted_key.decode()}

    with open(config_path, "w") as configfile:
        config.write(configfile)

def load_api_key():
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        encrypted_key = config["DEFAULT"]["api_key"].encode()
        decrypted_key = cipher_suite.decrypt(encrypted_key)
        return decrypted_key.decode()
    except Exception:
        return None

def delete_api_key():
    try:
        os.remove(config_path)
    except:
        pass
