from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.controller.auth_controller import auth_router
from app.core.log_middleware import LoggingMiddleware

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Custom Logging Middleware
app.add_middleware(LoggingMiddleware)

# Run the application
# To run: `uvicorn app.main:app --reload`
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)