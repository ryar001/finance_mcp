from contextlib import asynccontextmanager
from fastapi import FastAPI
from finance_mcp.main_mcp import mcp_server
from finance_mcp.routers import income_statement

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with mcp_server.lifespan_context(app):
     yield
    # Shutdown
    print("Shutting down the app...")

app = FastAPI(
    title="Financial MCP Server",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(income_statement.router, prefix="/api/v1", tags=["Income Statement"])

# Mount the MCP server
app.mount("/mcp", mcp_server.http_app())

@app.get("/")
def read_root():
    return {"message": "Free Finance MCP"}