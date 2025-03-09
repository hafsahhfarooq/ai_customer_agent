from fastapi import APIRouter
from services.llm import llm
from services.tools import track_order, process_return_request

agent_router = APIRouter()


def determine_intent(user_input: str) -> str:
    """
    Determines the customer's intent using the LLM.
    """
    prompt = f"""
    You are a customer service AI. Identify the intent of the following user query:
    "{user_input}"
    Respond with either "order_tracking" or "return_request".
    """

    response = llm.generate(prompt)
    return response.strip().lower()


def agent(user_input: str) -> str:
    """
    Main agent function to process user input and execute the correct tool.
    """
    intent = determine_intent(user_input)

    if "order_tracking" in intent:
        return track_order(user_input)  # Call the order tracking tool
    elif "return_request" in intent:
        return process_return_request(user_input)  # Call the return request tool
    else:
        return "Sorry, I didn't understand your request."


@agent_router.post("/customer-service/")
def customer_service(user_input: str):
    """
    Main API endpoint for customer service agent.
    """
    response = agent(user_input)
    return {"response": response}
