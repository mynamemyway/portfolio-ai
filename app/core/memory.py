# app/core/memory.py

import json
from pathlib import Path

import aiosqlite
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (
    BaseMessage,
    message_from_dict,
    message_to_dict,
)

# --- Constants ---

# Define the root directory of the project.
# Path(__file__) is the path to the current file (app/core/memory.py).
# .parent.parent navigates up two levels to the project root.
ROOT_DIR = Path(__file__).parent.parent.parent

# Directory for databases.
DB_DIR = ROOT_DIR / "app" / "db"

# Path to the SQLite database file for storing chat history.
CHAT_HISTORY_DB_PATH = DB_DIR / "chat_history.sqlite3"