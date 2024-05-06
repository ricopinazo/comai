import os
import tempfile
from pathlib import Path

from langchain_community.chat_message_histories import SQLChatMessageHistory

# from langchain.memory import ChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

temp_dir = tempfile.gettempdir()
session_id = os.getenv("TERM_SESSION_ID")
history_path: os.PathLike | None = None
if session_id:
    try:
        history_path = Path(os.path.join(temp_dir, session_id))
    except Exception:
        pass


def load_history(session_id: str) -> SQLChatMessageHistory | InMemoryChatMessageHistory:
    if history_path:
        return SQLChatMessageHistory(
            session_id=session_id, connection_string=f"sqlite:///{history_path}"
        )
    else:
        # return ChatMessageHistory()
        return InMemoryChatMessageHistory()


# class History:
#     def __init__(self, messages: List, filepath: Optional[os.PathLike] = None) -> None:
#         self.messages = messages
#         self.filepath = filepath

# @classmethod
# def load_from_file(cls, filepath: os.PathLike) -> History:
#     messages = []
#     try:
#         with open(filepath, "br") as history_file:
#             messages = pickle.load(history_file)
#     except Exception:
#         pass
#     return History(messages, filepath)

# @classmethod
# def create_local(cls) -> History:
#     return History([], None)

# def append_user_message(self, request: str) -> None:
#     user_message = {"role": "user", "content": request}
#     self.messages += [user_message]

# def append_assistant_message(self, command: str) -> None:
#     content = f"""COMMAND {command} END"""
#     assistant_message = {"role": "user", "content": content}
#     self.messages += [assistant_message]

# def get_messages(self) -> List:
#     return self.messages

# def checkpoint(self) -> None:
#     if self.filepath:
#         with open(self.filepath, "bw") as history_file:
#             pickle.dump(self.messages, history_file)

# def copy(self) -> History:
#     return History(copy(self.messages), self.filepath)
