from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def percentage_tool(percentage: str, tool_context: ToolContext) -> dict:
    """Adds percentage to state.

    Returns:
        A confirmation message
    """
    print(f"--- Tool: percentage_tool called ---")

    tool_context.state["academic_percentage"] = percentage

    return {
        "action": "percentage_tool",
        "message": "percentage saved",
    }

def lor_store(letters_of_recommentation: str,tool_context: ToolContext) -> dict:
    """ save the pdf link
    Returns:
        A confirmation message
    """

    tool_context.state["letters_of_recommendation"] = letters_of_recommentation

    return {
        "action": "lor_store",
        "message": "Letters of recommentation saved",
    }
    
def test_score_store(score: str ,tool_context: ToolContext) -> dict:
    """ save the score
    Returns:
        A confirmation message
    """

    tool_context.state["standardised_test_score"] = score

    return {
        "action": "test_store_store",
        "message": "Standardised Test Score saved",
    }

def budget_store(budget: str,tool_context: ToolContext) -> dict:
    """ save the budget
    Returns:
        A confirmation message
    """

    tool_context.state["budget"] = budget

    return {
        "action": "budget_store",
        "message": "Budget saved",
    }


    

user_info = Agent(
    name="user_info",
    model="gemini-2.0-flash-001",
    description="Selects College",
    instruction="""
        You are an agent who asks and stores user's information in the state.
        Your job is to get information on the following:
            - Academic Percentage (*)
              (use percentage_tool Tool for storing percentage)
            - Letters of Recommendation
              (use lor_store Tool for storing letter of recommendation)
            - Standardised Test Scores
              (use test_score_store Tool for storing  Standardised Test Scores)
            - Budget (*)
              (use budget_store Tool for storing Budget)
        Mention that the Letter of Recommendation should be a public google drive link
    """,
    tools=[
        percentage_tool,lor_store,test_score_store,budget_store
    ]
)