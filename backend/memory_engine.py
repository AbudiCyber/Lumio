"""
Memory Engine v1

Central memory layer for Lumio AI.

Responsible for managing conversation memory,
project memory, and future long-term memory.
"""


class MemoryEngine:
    """
    Central memory manager.

    This class will become the single entry point
    for every type of memory used inside Lumio.
    """

    def __init__(self):
        """Initialize memory containers."""

        self.short_term_memory = []
        self.project_memory = {}
        self.user_preferences = {}
        self.long_term_memory = {}

    def save_message(self, role, content):
        """
        Save a conversation message.
        """

        self.short_term_memory.append({
            "role": role,
            "content": content
        })

    def get_messages(self):
        """
        Return conversation history.
        """

        return self.short_term_memory

    def clear_messages(self):
        """
        Clear conversation history.
        """

        self.short_term_memory.clear()

    def save_project_data(self, key, value):
        """
        Save project-related information.
        """

        self.project_memory[key] = value

    def get_project_data(self, key):
        """
        Retrieve project information.
        """

        return self.project_memory.get(key)

    def save_user_preference(self, key, value):
        """
        Save user preference.
        """

        self.user_preferences[key] = value

    def get_user_preference(self, key):
        """
        Return user preference.
        """

        return self.user_preferences.get(key)

    def health(self):
        """
        Return memory engine status.
        """

        return {
            "status": "ready",
            "version": "1.0.0",
            "messages": len(self.short_term_memory),
            "project_items": len(self.project_memory),
            "preferences": len(self.user_preferences)
        }