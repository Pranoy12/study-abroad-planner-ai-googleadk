
from google.adk.agents import Agent
from google.adk.tools import google_search

visa_agent= Agent(
    name="visa_agent",
    model="gemini-2.0-flash-001",
    description="visa process steps",
    instruction="""
        You are an agent that takes required necessary inputs from the user so that you could provide student visa application process.
        Generate a step by step process for student visa application.
        You can use the google_search tool to find the perfect answer for the user.
        
        delegate to pdf_visa sub-agent after output generation
        
    """,
    tools=[
        google_search
    ],
    output_key="visa_process_key"
)





# # from google.adk.agents import Agent
# # from google.adk.tools import google_search




# visa_agent= Agent(
#     name="visa_agent",
#     model="gemini-2.0-flash-001",
#     description="visa process steps",
#     instruction="""
#         You are an agent that takes required necessary inputs from the user so that you could provide student visa application process.
#         Generate a step by step process for student visa application.
#         You can use the google_search tool to find the perfect answer for the user.
        
        
#         Delegate back to root_agent after output generated.
#     """,
#     tools=[
#         google_search
#     ]
# )