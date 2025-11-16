"""
Storage module for managing prompt history
Uses JSON file for persistent storage
"""
import json
import os
from typing import List, Dict
from datetime import datetime
from pathlib import Path

HISTORY_FILE = "history.json"


def load_history() -> Dict[str, List[Dict]]:
    """
    Load history from JSON file
    
    Returns:
        Dictionary with username as key and list of history items as value
    """
    if not os.path.exists(HISTORY_FILE):
        return {}
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading history: {e}")
        return {}


def save_history(history: Dict[str, List[Dict]]) -> None:
    """
    Save history to JSON file
    
    Args:
        history: Dictionary of user histories to save
    """
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving history: {e}")


def add_to_history(username: str, prompt: str, response: str) -> None:
    """
    Add a new prompt/response pair to user's history
    
    Args:
        username: Username of the user
        prompt: The prompt text
        response: The model's response
    """
    history = load_history()
    
    # Initialize user's history if it doesn't exist
    if username not in history:
        history[username] = []
    
    history_item = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    }
    
    # Add to user's history
    history[username].append(history_item)
    
    save_history(history)


def get_user_history(username: str) -> List[Dict]:
    """
    Retrieve all history for a specific user
    
    Args:
        username: Username to get history for
    
    Returns:
        List of history items (dictionaries with timestamp, prompt, response)
    """
    history = load_history()
    return history.get(username, [])


def clear_user_history(username: str) -> None:
    """
    Clear all history for a specific user (optional utility function)
    
    Args:
        username: Username whose history to clear
    """
    history = load_history()
    if username in history:
        history[username] = []
        save_history(history)