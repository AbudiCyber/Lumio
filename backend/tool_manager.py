"""
Tool Manager v1

Responsible for registering and executing tools.

The Tool Manager does not implement tools itself.
It only manages them.
"""


class ToolManager:
    """
    Central registry for all available tools.
    """

    def __init__(self):
        self.tools = {}

    def register_tool(self, name, tool):
        """
        Register a tool.
        """

        self.tools[name] = tool

    def get_tool(self, name):
        """
        Return a registered tool.
        """

        return self.tools.get(name)

    def execute(self, name, *args, **kwargs):
        """
        Execute a registered tool.
        """

        tool = self.get_tool(name)

        if tool is None:
            return {
                "status": "error",
                "message": f"Tool '{name}' not found."
            }

        return tool(*args, **kwargs)

    def list_tools(self):
        """
        Return all registered tools.
        """

        return list(self.tools.keys())

    def health(self):
        """
        Tool Manager status.
        """

        return {
            "status": "ready",
            "registered_tools": len(self.tools),
            "version": "1.0.0"
        }