from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import agent_tool
from .sub_agents.college_finder import college_finder
from .sub_agents.college_selector import college_selector
from .sub_agents.user_info import user_info
from .sub_agents.resume_builder import resume_builder
from .sub_agents.weather_agent import weather_agent
from .sub_agents.visa_agent import visa_agent
from .sub_agents.pdf_visa import pdf_visa

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
            - academic_percentage: {academic_percentage},
            - letters_of_recommendation: {letters_of_recommendation},
            - budget:{budget},
            - standardised_test_score:{standardised_test_score},
            - selected_college : {selected_college}
            
            
        You have access to the following tools:
            - update_user_name
            - clear_chat_history
            - college_finder
            - visa_agent
            - weather_agent
            
        You have access to the following sub agents:
            - college_selector
            - user_info
            - resume_builder
            - pdf_visa

            
            
        GUIDLINES:
            1. Greet the user first using the following guidelines:
                - Use friendly and proffesional tone when greeting the user.
                - Be polite always.
                - If you don't know the user's name from state {user_name} , greet them generally and ask for their name. 
                - Once you get a new user_name, store that inside the session state using update_user_name tool
                - If you already know the user's name, greet them using their name
            2.Immediatly after Greeting, check if any of these states are empty->{academic_percentage},{letters_of_recommendation},{budget},{standardised_test_score}. if empty, Ask the user to input those details and use the user_info sub-agent to add the informations to the states.
            3. If the user wants to clear their chat history (e.g, 'clear', 'clear chat' etc) use the tool clear_chat_history
            4. Use college_finder if the user asks to find colleges or ask to recommend colleges
            5. If user says to add or selects particular college (e.g, 'Select Stanford'), use the college_selector sub-agent to add the college to state
            6. If user ask to build a resume , use the resume_builder sub-agent to generate resume and store to the database.
            7. if user want to know about the visa application process , use the visa_agent sub-agent to generate the visa process and immediately after visa_agent use pdf_visa sub-agent to store visa application process to pdf in db 
            8. if user want to know about the weather, use weather_agent.
    """,
    tools=[
        update_user_name,
        clear_chat_history,
        agent_tool.AgentTool(agent=college_finder),
        agent_tool.AgentTool(agent=visa_agent),
        agent_tool.AgentTool(agent=weather_agent)
    ],
    sub_agents=[
        college_selector,
        user_info,
        resume_builder,
        pdf_visa
    ]
)
