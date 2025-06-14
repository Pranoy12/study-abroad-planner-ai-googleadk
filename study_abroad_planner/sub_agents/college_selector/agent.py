from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def college_selction(college: str, tool_context: ToolContext) -> dict:
    """Adds selected college to state.

    Returns:
        A confirmation message
    """
    print(f"--- Tool: college_selction called ---")

    tool_context.state["selected_college"] = college

    return {
        "action": "college_selction",
        "message": "College Selected",
    }

college_selector = Agent(
    name="college_selcetor",
    model="gemini-2.0-flash-001",
    description="Selects College",
    instruction="""
        You are a college selctor agent.
        Your job is to add the college selected by the user to the session using college_selction tool.
    """,
    tools=[
        college_selction
    ]
)