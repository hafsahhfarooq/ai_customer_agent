from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database  import get_db
from db.models import Order

# Create router for Order Tracking
ordertracking_router = APIRouter()

# Get order details by order number
@ordertracking_router.get("/orders/{order_number}")
def get_order(order_number: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_number": order.order_number,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "status": order.status,
        "estimated_delivery": order.estimated_delivery.strftime("%Y-%m-%d") if order.estimated_delivery else "N/A"
    }

# Update order status
@ordertracking_router.put("/orders/{order_number}/status")
def update_order_status(order_number: str, new_status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = new_status
    db.commit()
    return {"message": "Order status updated successfully", "new_status": order.status}

# Get orders by customer phone
@ordertracking_router.get("/orders/customer/phone/{customer_phone}")
def get_orders_by_phone(customer_phone: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.customer_phone == customer_phone).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this customer")

    return [{"order_number": order.order_number, "status": order.status} for order in orders]

# Get orders by customer name
@ordertracking_router.get("/orders/customer/name/{customer_name}")
def get_orders_by_name(customer_name: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.customer_name.ilike(f"%{customer_name}%")).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this customer")

    return [{"order_number": order.order_number, "status": order.status} for order in orders]
