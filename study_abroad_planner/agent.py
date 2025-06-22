from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.college_finder import college_finder
from .sub_agents.college_selector import college_selector

def clear_chat_history(tool_context: ToolContext) -> dict:
    """Clear the chat history.

    Returns:
        A confirmation message
    """
    print(f"--- Tool: clear_chat_history called ---")

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
            
        You have access to the following tools:
            - update_user_name
            - clear_chat_history
            - college_finder
            
        You have access to the following sub agents:
            - college_selector
            
        GUIDLINES:
            1. Greet the user first using the following guidelines:
                - Use friendly and proffesional tone when greeting the user.
                - Be polite always.
                - If you don't know the user's name from state {user_name} , greet them generally and ask for their name. 
                - Once you get a new user_name, store that inside the session state using update_user_name tool
                - If you already know the user's name, greet them using their name
            2. If the user wants to clear their chat history (e.g, 'clear', 'clear chat' etc) use the tool clear_chat_history
            3. Use college_finder if the user asks to find colleges
            4. If user says to add/select/choose a college (e.g, 'Select Stanford'), use the college_selector sub-agent to add the college to state
            5. After a college is selected output to the user that the college has been selected/added.
    """,
    tools=[
        update_user_name,
        clear_chat_history,
        AgentTool(college_finder)
    ],
    sub_agents=[
        college_selector
    ]
)
