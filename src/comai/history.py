import os
import tempfile
from pathlib import Path

from langchain_community.chat_message_histories import SQLChatMessageHistory
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
        return InMemoryChatMessageHistory()
