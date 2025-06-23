import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

# IMPORT root agent
from study_abroad_planner.agent import root_agent as study_abroad_planner
from utils import Colors, call_agent_async

load_dotenv()

# DB
dburl = "sqlite:///./user_data.db"
session_service = DatabaseSessionService(db_url=dburl)

initial_state = {
    "user_name": "",
    "selected_college": [],
    "interaction_history": [],
    "academic_percentage": "",
    "letters_of_recommendation": "",
    "budget":"",
    "standardised_test_score":""
    
}

async def main():
    APP_NAME = "Study Abroad Planner"
    USER_ID = "v05"
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")
        
    runner = Runner(
        agent=study_abroad_planner,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    print("\nWELCOME TO STUDY ABROAD PLANNER!")
    print("Your DATA will be stored in the session state.")

    # print(f"{Colors.CYAN}{Colors.BOLD}{await call_agent_async(runner, USER_ID, SESSION_ID, 'Hi')}{Colors.RESET}")

    while True:
        print("Type 'exit' or 'quit' to end chat")
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Ending chat. Goodbye!")
            break
        
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)
    
if __name__ == "__main__":
    asyncio.run(main())