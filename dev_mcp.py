from fastmcp import FastMCP
import asyncio
import os
from pathlib import Path
from typing import Optional, Literal

# Initialize a standalone MCP server for development tools
mcp = FastMCP("Dev Tools")

# Path to the shell script (assumed to be in the same directory as this file)
TOOLS_SCRIPT_PATH = str(Path(__file__).resolve().parent / "ai-tracker.sh")

@mcp.tool()
async def run_ai_tracker(
    force: bool = False,
    version_bump: Literal["major", "minor", "patch", "none"] = "patch",
    commit_hash: Optional[str] = None
) -> str:
    """
    Run the ai-tracker.sh script to track changes, generate AI summaries, and commit.

    Args:
        force: Ignore AI-detected errors and proceed with commit (default: False).
        version_bump: How to bump the version (default: "patch").
        commit_hash: Optional commit hash to generate diff from.
    """
    
    # Construct command arguments
    args = [TOOLS_SCRIPT_PATH]
    
    if force:
        args.append("force")
        
    if commit_hash:
        args.extend(["-r", commit_hash])
        
    if version_bump:
        args.extend(["-v", version_bump])
        
    try:
        # Check if script exists and is executable
        if not os.path.exists(TOOLS_SCRIPT_PATH):
            return f"Error: Script not found at {TOOLS_SCRIPT_PATH}"
            
        if not os.access(TOOLS_SCRIPT_PATH, os.X_OK):
            # Try to make it executable
            try:
                os.chmod(TOOLS_SCRIPT_PATH, 0o755)
            except Exception as e:
                return f"Error: Script is not executable and chmod failed: {e}"

        # Prepare environment with /opt/homebrew/bin in PATH
        env = os.environ.copy()
        current_path = env.get("PATH", "")
        if "/opt/homebrew/bin" not in current_path:
            env["PATH"] = f"/opt/homebrew/bin:{current_path}"

        # Execute the script
        # We need to run this in the project root
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.dirname(TOOLS_SCRIPT_PATH),
            env=env
        )
        
        stdout, stderr = await process.communicate()
        
        output = ""
        if stdout:
            output += f"STDOUT:\n{stdout.decode()}\n"
        if stderr:
            output += f"STDERR:\n{stderr.decode()}\n"
            
        if process.returncode != 0:
            return f"Command failed with return code {process.returncode}:\n{output}"
            
        return f"Success:\n{output}"

    except Exception as e:
        return f"Error running ai-tracker: {str(e)}"

if __name__ == "__main__":
    # This allows running the server directly
    mcp.run()
