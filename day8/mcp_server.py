"""Optional: exposes the three tools over MCP. Needs: pip install mcp"""
from mcp.server.fastmcp import FastMCP
import agent_core as core

mcp = FastMCP("requisition-agent")

@mcp.tool()
def check_supplier(name: str) -> str:
    """Return supplier status: good, poor, new or unknown."""
    return core.check_supplier(name)

@mcp.tool()
def create_po(requisition_id: str, supplier: str, amount: float) -> dict:
    """Create a PO. Writes only to po_created.json."""
    return core.create_po(requisition_id, supplier, amount)

@mcp.tool()
def route_to_manager(requisition_id: str, reason: str) -> dict:
    """Send a requisition to the manager with a reason."""
    return core.route_to_manager(requisition_id, reason)

if __name__ == "__main__":
    mcp.run()
