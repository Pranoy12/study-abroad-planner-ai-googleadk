from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_user_name called with '{name}' ---")

    # Get current name from state
    old_name = tool_context.state.get("user_name", "")

    # Update the name in state
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"Updated your name to: {name}",
    }
    
greetings_agent = Agent(
    name="greetings_agent",
    model="gemini-2.0-flash-001",
    description="Greeting agent",
    instruction="""
        You are a greeting agent. Use the following guidelines to greet the user

        user name: {user_name}
        
        Guidelines:
            - Use friendly and proffesional tone when greeting the user.
            - Be polite always.
            - If you don't know the user's name from state , greet them generally and ask for their name. Store their name inside the session using update_user_name tool
            - If you already know the user's name, greet them using their name and delegate back to root_agent
            - If user asks to update name, don't greet them - do the needful accordingly
            - If user asks anything else, delegate to root_agent immediately
        
        IMPORTANT: After successfully greeting or updating the session state, always return control back to root_agent
    """,
    tools=[
        update_user_name
    ]
)