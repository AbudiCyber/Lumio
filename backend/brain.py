"""
Brain Orchestrator v1

The central coordinator for Lumio AI.
Responsible for connecting all engines together.
"""

from ai_engine import AIEngine
from memory_engine import MemoryEngine


class Brain:

    def __init__(self):
        self.ai = AIEngine()
        self.memory = MemoryEngine()

    def process_message(self, message):

        # Save user message
        self.memory.save_message("user", message)

        # Generate AI response
        response = self.ai.generate(message)

        # Save assistant response
        self.memory.save_message("assistant", response)

        return response

    def health(self):

        return {
            "brain": "online",
            "memory": self.memory.health(),
        }