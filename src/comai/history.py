import os
import pickle
from typing import Optional, List


class History:
    def __init__(self, messages: List, filepath: Optional[os.PathLike] = None) -> None:
        self.messages = messages
        self.filepath = filepath

    @classmethod
    def load_from_file(cls, filepath: os.PathLike):
        messages = []
        try:
            with open(filepath, "br") as history_file:
                messages = pickle.load(history_file)
        except Exception:
            pass
        return cls(messages, filepath)

    @classmethod
    def create_local(cls):
        return cls([], None)

    def append_user_message(self, request: str) -> None:
        user_message = {"role": "user", "content": request}
        self.messages.append(user_message)

    def append_assistant_message(self, command: str) -> None:
        content = f"""COMMAND {command} END"""
        assistant_message = {"role": "user", "content": content}
        self.messages.append(assistant_message)

    def get_messages(self) -> List:
        return self.messages

    def checkpoint(self) -> None:
        if self.filepath:
            with open(self.filepath, "bw") as history_file:
                pickle.dump(self.messages, history_file)
