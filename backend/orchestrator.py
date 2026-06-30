"""
Brain Orchestrator v1

Coordinates all AI engines.
"""

from backend.goal_engine import GoalEngine
from backend.context_engine import ContextEngine
from backend.ai_engine import AIEngine


class BrainOrchestrator:

    def __init__(self):

        self.goal_engine = GoalEngine()
        self.context_engine = ContextEngine()
        self.ai_engine = AIEngine()

    def run(self, message):

        goal = self.goal_engine.detect_goal(message)

        context = self.context_engine.build(
            message=message,
            goal=goal
        )

        response = self.ai_engine.generate(context)

        return {
            "goal": goal,
            "context": context,
            "response": response
        }

    def health(self):

        return {
            "status": "ready",
            "goal": self.goal_engine.health(),
            "context": self.context_engine.health(),
            "ai": self.ai_engine.health()
        }