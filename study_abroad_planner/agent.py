from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# Importing sub-agents
from .sub_agents.greetings_agent import greetings_agent

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

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A study abroad planner agent',
    instruction="""
        You are a study abroad planner. Your work is to take user query and delgate it to the sub-agents you have.
        If the input is "Hi" or something similar, use greeting_agent
        
        Use the greetings_agent:
            - to greet the user.
            - if the user wants to update their name (e.g, 'update my name to', 'change my name to' etc).
        
        Sub-Agents:
            1. greetings_agent
            
            
        GUIDLINES:
            1. Greet the user first
            2. If the user wants to clear their chat history (e.g, 'clear', 'clear chat' etc) use the tool clear_chat_history
    """,
    tools=[
        clear_chat_history    
    ],
    sub_agents=[
        greetings_agent
    ]
)
