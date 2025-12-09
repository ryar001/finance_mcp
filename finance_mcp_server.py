import sys
import os
from finance_mcp.main_mcp import mcp_server

# Redirect stderr to a log file to prevent pollution of the MCP channel
# and to capture logs that might otherwise be lost or cause issues.
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_server.log")
sys.stderr = open(log_file_path, "a")

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    mcp_server.run()
