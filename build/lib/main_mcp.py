from fastapi import FastAPI
from fastmcp import APIRouter
from src.tools.income_statement_tool import IncomeStatementTool
from src.services.financial_data import list_available_models

app = FastAPI(
    title="Financial MCP Server",
    version="1.0.0",
)

mcp_router = APIRouter(
    tools=[
        IncomeStatementTool(),
    ]
)

app.include_router(mcp_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await list_available_models()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial MCP Server with MCP Tools"}

