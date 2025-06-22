from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# def college_selction(college: str, tool_context: ToolContext) -> dict:
#     """Adds selected college to state.

#     Returns:
#         A confirmation message
#     """
#     print(f"--- Tool: college_selction called ---")

#     tool_context.state["selected_college"] = college

#     return {
#         "action": "college_selction",
#         "message": "College Selected",
#     }
    
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

college_selector = Agent(
    name="college_selcetor",
    model="gemini-2.0-flash-001",
    description="Selects College",
    instruction="""
        You are a college selctor agent.
        Your job is to add the college selected by the user to the session via the output_key.
        If user asks to show/display his selected/chosen colleges, retrieve it from the state {selected_college} and show it to user
        
        IMPORTANT: The output should be of the format
        {
            "{"collegeName"}"
        }
        
        Delegate back to root_agent after output generated.
    """,
    # tools=[
    #     college_selction
    # ],
    output_key="selected_college"
)