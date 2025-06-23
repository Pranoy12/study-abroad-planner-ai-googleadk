from google.adk.agents import Agent
from google.adk.tools import google_search

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash-001",
    description="provide the weather",
    instruction="""
        You are a weather outputting agent, where you can ask the user which country's weather you need and fetch that particular country's weather using google_search tool and provide to user 
    """,
    tools=[
        google_search
    ]
)
