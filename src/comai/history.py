from __future__ import annotations

import os
import pickle
from copy import copy
from typing import Optional, List


class History:
    def __init__(self, messages: List, filepath: Optional[os.PathLike] = None) -> None:
        self.messages = messages
        self.filepath = filepath

    @classmethod
    def load_from_file(cls, filepath: os.PathLike) -> History:
        messages = []
        try:
            with open(filepath, "br") as history_file:
                messages = pickle.load(history_file)
        except Exception:
            pass
        return History(messages, filepath)

    @classmethod
    def create_local(cls) -> History:
        return History([], None)

    def append_user_message(self, request: str) -> None:
        user_message = {"role": "user", "content": request}
        self.messages += [user_message]

    def append_assistant_message(self, command: str) -> None:
        content = f"""COMMAND {command} END"""
        assistant_message = {"role": "user", "content": content}
        self.messages += [assistant_message]

    def get_messages(self) -> List:
        return self.messages

    def checkpoint(self) -> None:
        if self.filepath:
            with open(self.filepath, "bw") as history_file:
                pickle.dump(self.messages, history_file)

    def copy(self) -> History:
        return History(copy(self.messages), self.filepath)
