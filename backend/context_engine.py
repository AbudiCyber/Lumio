"""
Context Engine v1

Collects all context required before AI execution.
"""


class ContextEngine:
    """
    Responsible for building the execution context
    before sending data to the AI Engine.
    """

    def __init__(self):
        self.context = {}

    def build(
        self,
        message,
        goal=None,
        memory=None,
        project=None
    ):
        """
        Build execution context.
        """

        self.context = {
            "message": message,
            "goal": goal,
            "memory": memory,
            "project": project
        }

        return self.context

    def get(self):
        """
        Return current context.
        """
        return self.context

    def clear(self):
        """
        Clear context.
        """
        self.context = {}

    def health(self):
        """
        Engine status.
        """

        return {
            "status": "ready",
            "context_items": len(self.context),
            "version": "1.0.0"
        }