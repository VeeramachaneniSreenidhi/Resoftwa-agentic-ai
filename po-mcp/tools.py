import csv
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PO-Checker-Server")

@mcp.tool()
def check_po_status(po_number: str) -> dict:
    """Look up PO number in local po_list.csv data source."""
    try:
        with open("po_list.csv", mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["po_number"].strip() == po_number.strip():
                    return {
                        "exists": True, 
                        "status": row["status"], 
                        "vendor": row["vendor"],
                        "total_amount": row["total_amount"]
                    }
    except Exception as e:
        return {"exists": False, "error": str(e)}
    return {"exists": False, "status": "NOT_FOUND"}
