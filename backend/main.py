# backend/main.py
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .database import init_db
from .routers import auth, transactions, investments, goals, wealth, insights, ai_chat, calendar

app = FastAPI(title="SecureWealth Twin API", version="1.0.0")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Time: {process_time:.4f}s")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
async def health_check():
    return {"status": "ok", "ai_provider": settings.AI_PROVIDER}

@app.get("/demo/personas")
async def get_demo_personas():
    return [
        {"id": 1, "name": "Priya Sharma", "role": "Software Engineer", "theme": "Moderate"},
        {"id": 2, "name": "Ramesh Kulkarni", "role": "Business Owner", "theme": "Conservative"},
        {"id": 3, "name": "Ananya Iyer", "role": "First Job", "theme": "Aggressive"}
    ]

@app.get("/demo/reset/{persona}")
async def reset_demo(persona: str):
    # This would call seed_db logic
    return {"message": f"Demo reset for {persona} initiated"}

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error: " + str(exc)},
    )

# Placeholder includes for routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(investments.router, prefix="/investments", tags=["investments"])
app.include_router(goals.router, prefix="/goals", tags=["goals"])
app.include_router(wealth.router, prefix="/wealth", tags=["wealth"])
app.include_router(insights.router, prefix="/insights", tags=["insights"])
app.include_router(ai_chat.router, prefix="/ai_chat", tags=["ai"])
app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
