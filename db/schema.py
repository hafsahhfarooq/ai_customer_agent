from pydantic import BaseModel

class ReturnRequest(BaseModel):
    order_id: str
    reason: str
