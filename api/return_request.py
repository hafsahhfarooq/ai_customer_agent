from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schema import ReturnRequest
from db.database import get_db
from db.models import Order
from services.rag_utils import retrieve_policy

returnrequest_router = APIRouter()

THRESHOLD = 0.75  # Stricter similarity threshold


def process_return(request: ReturnRequest, db: Session):
    """
    Processes a return request by verifying order existence, checking return policy,
    and handling partial returns with improved logging.
    """

    # Check if order exists
    order = db.query(Order).filter(Order.order_number == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")


    # Retrieve the most relevant return policy
    relevant_policy, distance = retrieve_policy(request.reason)

    if distance > THRESHOLD:
        return {
            "message": "Return request denied: No matching return policy",
            "policy_reference": relevant_policy,
            "distance": distance
        }

    db.add(return_request_log)
    db.commit()

    return {
        "message": "Return request submitted successfully",
        "order_id": request.order_id,
        "status": "Pending",
        "policy_reference": relevant_policy
    }


@returnrequest_router.post("/return-request/")
def return_request_api(request: ReturnRequest, db: Session = Depends(get_db)):
    """
    API endpoint for handling return requests.
    Calls process_return() for logic.
    """
    return process_return(request, db)
