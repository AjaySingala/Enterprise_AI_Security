"""
===============================================================================
Enterprise AI Gateway (EAIG)

Conversation Storage

Version:
    2.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from common.filename import make_safe_filename

###############################################################################
# Root Folder
###############################################################################
ROOT_FOLDER = Path("conversations")

###############################################################################
def get_conversation_folder() -> Path:
    """
    Returns today's conversation folder.
    """

    folder = ROOT_FOLDER / datetime.now().strftime("%Y-%m-%d")
    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return folder

###############################################################################
def get_conversation_filename(
    title: str,
    extension: str = "json",
) -> Path:
    """
    Returns a unique filename for a conversation.

    Example:

    conversations/
        2026-07-02/
            20260702_214533_What_is_RAG.json
    """
    safe_title = make_safe_filename(
        title,
        max_length=60,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"{timestamp}_{safe_title}.{extension}"
    )

    return get_conversation_folder() / filename

###############################################################################
def list_conversations() -> list[Path]:
    """
    Return all saved conversations, newest first.
    """
    if not ROOT_FOLDER.exists():
        return []

    conversations = sorted(
        ROOT_FOLDER.rglob("*.json"),
        reverse=True,
    )

    return conversations

###############################################################################
from datetime import datetime

def choose_conversation() -> Path | None:
    """
    Interactive conversation chooser.
    """
    conversations = list_conversations()

    if not conversations:
        print()
        print("No saved conversations.")
        return None

    print()
    print("=" * 90)
    print("Saved Conversations")
    print("=" * 90)
    print()

    for index, conversation in enumerate(conversations, start=1):
        stem = conversation.stem

        #
        # Expected format:
        #
        # 20260702_214533_What_is_RAG
        #
        try:
            date_part, time_part, title = stem.split(
                "_",
                2,
            )

            timestamp = datetime.strptime(
                f"{date_part}_{time_part}",
                "%Y%m%d_%H%M%S",
            )

            display_date = timestamp.strftime(
                "%d-%b-%Y %H:%M:%S"
            )

        except Exception:
            title = stem
            display_date = ""

        print(f"{index:2}. {title}")

        if display_date:
            print(f"    {display_date}")

        print()

    while True:
        choice = input(
            "Select conversation (0 to cancel): "

        ).strip()

        if not choice.isdigit():
            continue

        choice = int(choice)

        if choice == 0:
            return None

        if 1 <= choice <= len(conversations):
            return conversations[choice - 1]
