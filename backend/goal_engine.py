"""
Goal Engine v1

Detects the user's primary objective before execution.
"""


class GoalEngine:

    def __init__(self):
        self.goal = None

    def detect_goal(self, message: str):

        text = message.lower()

        if any(word in text for word in [
            "code",
            "python",
            "script",
            "program",
            "function"
        ]):
            self.goal = "coding"

        elif any(word in text for word in [
            "explain",
            "what",
            "why",
            "how"
        ]):
            self.goal = "education"

        elif any(word in text for word in [
            "plan",
            "roadmap",
            "strategy"
        ]):
            self.goal = "planning"

        elif any(word in text for word in [
            "fix",
            "error",
            "bug"
        ]):
            self.goal = "debugging"

        else:
            self.goal = "general"

        return self.goal

        def health(self):

        return {
            "status": "ready",
            "goal": self.goal
        }