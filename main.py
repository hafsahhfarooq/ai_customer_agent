from fastapi import FastAPI
from db.database import engine, Base
from api.order_tracking import ordertracking_router
from api.return_request import returnrequest_router
from api.voice_processing import voiceprocessing_router
from api.agent import agent_router
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI(title="E-Commerce Customer Service Agent")

# Enable CORS for frontend (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(ordertracking_router, prefix="/tracking", tags=["Order Tracking"])
app.include_router(returnrequest_router, prefix="/returns", tags=["Return Requests"])
app.include_router(voiceprocessing_router, prefix="/voice", tags=["Voice Process"])
app.include_router(agent_router, prefix="/agent", tags=["Agent"])

# Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the E-Commerce Customer Service API!"}
