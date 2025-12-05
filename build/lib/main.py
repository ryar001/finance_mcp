from fastapi import FastAPI
from src.routers import income_statement
from src.services.financial_data import list_available_models

app = FastAPI(
    title="Financial MCP Server",
    version="1.0.0",
)

app.include_router(income_statement.router, prefix="/api/v1", tags=["Income Statement"])

@app.on_event("startup")
async def startup_event():
    await list_available_models()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial MCP Server"}

