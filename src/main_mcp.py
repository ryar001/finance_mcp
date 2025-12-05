from fastmcp import FastMCP
from src.main import app


mcp = FastMCP.from_fastapi(
    app=app,
    name="Financial MCP",
)

if __name__ == "__main__":
    mcp.run()