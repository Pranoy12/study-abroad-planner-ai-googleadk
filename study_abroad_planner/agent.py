from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def clear_chat_history(tool_context: ToolContext) -> dict:
    """Clear the chat history.

    Returns:
        A confirmation message
    """
    print(f"--- Tool: clear_chat_history called ---")

    # Update the name in state
    tool_context.state["interaction_history"] = []

    return {
        "action": "clear_chat_history",
        "message": "Cleared Chat History",
    }

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
    
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A study abroad planner agent',
    instruction="""
        You are a study abroad planner. 
        Your job is to take user query and delgate it according to the context to the sub-agents you have.
        If the query is more general and doesn't fit with any sub-agents, try to answer it yourself.
        
        State values present:
            - user name: {user_name}
            - interaction history: {interaction_history}
            
        GUIDLINES:
            1. Greet the user first using the following guidelines:
                - Use friendly and proffesional tone when greeting the user.
                - Be polite always.
                - If you don't know the user's name from state {user_name} , greet them generally and ask for their name. 
                - Once you get a new user_name, store that inside the session state using update_user_name tool
                - If you already know the user's name, greet them using their name
            2. If the user wants to clear their chat history (e.g, 'clear', 'clear chat' etc) use the tool clear_chat_history
    """,
    tools=[
        update_user_name,
        clear_chat_history    
    ]
)
