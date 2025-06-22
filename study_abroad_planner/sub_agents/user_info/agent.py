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
    
# def display_college(college: str, tool_context: ToolContext) -> dict:
#     """Displays selected college to state.

#     Returns:
#         A confirmation message
#     """
#     print(f"--- Tool: display_college called ---")

#     tool_context.state["selected_college"]

#     return {
#         "action": "college_selction",
#         "message": "College Selected",
#     }

user_info = Agent(
    name="user_info",
    model="gemini-2.0-flash-001",
    description="Selects College",
    instruction="""
        You are an agent who asks and stores user's information in the state.
        Your job is to get information on the following:
            - Academic Percentage (*)
            - Letters of Recommendation
            - Statement of Purpose
            - Resume/CV (*)
            - Standardised Test Scores
            - Budget (*)
    """,
    tools=[
        college_selction
    ]
)