import re
from api.order_tracking import get_order  # Import order tracking function
from api.return_request import process_return  # Import return request function

def extract_order_number(user_input):
    """
    Extracts the order number from the user input using regex.
    """
    match = re.search(r'\b\d{5,}\b', user_input)  # Order number: 5+ digits
    return match.group() if match else None

def track_order(user_input):
    """
    Extracts order number from input and fetches order status.
    """
    order_number = extract_order_number(user_input)  # Extract order number
    if not order_number:
        return "Please provide a valid order number."

    order_info = get_order(order_number)  # Query order tracking

    if "error" in order_info:
        return f"Error: {order_info['error']}"

    return f"Order #{order_info['order_number']} is currently '{order_info['status']}'. Estimated delivery: {order_info['estimated_delivery']}."

def process_return_request(user_input):
    """
    Handles return requests.
    """
    return_info = process_return(user_input)  # Process return request

    if "error" in return_info:
        return f"Error: {return_info['error']}"

    return f"Return request for order #{return_info['order_id']} has been processed: {return_info['status']}."
