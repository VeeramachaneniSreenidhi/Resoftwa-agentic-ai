"""MCP server exposing the invoice validation tool. Needs: pip install mcp"""
from mcp.server.fastmcp import FastMCP
import inv_tools

mcp = FastMCP("invoice-validator")


@mcp.tool()
def validate_invoice(invoice: dict, seen_invoice_nos: list[str] | None = None) -> dict:
    """Validate one invoice against the PO master. Read-only; never posts.
    Returns status 'clean' or 'exception' with a list of reasons."""
    return inv_tools.validate_invoice(invoice, seen_invoice_nos or [])


if __name__ == "__main__":
    mcp.run()
