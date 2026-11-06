## Application Details
|               |
| ------------- |
|**Generation Date and Time**<br>Wed Oct 28 2026 17:27:20 GMT+0000 (Coordinated Universal Time)|
|**App Generator**<br>SAP Fiori Application Generator|
|**App Generator Version**<br>1.34.0|
|**Generation Platform**<br>SAP Business Application Studio|
|**Template Used**<br>List Report Page V2|
|**Service Type**<br>SAP System (ABAP On-Premise)|
|**Service URL**<br>http://hilmar.sapvista.com:50000/sap/opu/odata/sap/ZSUI_SALES_ANALYSIS_BIND|
|**Module Name**<br>project2|
|**Application Title**<br>App Title|
|**Namespace**<br>|
|**UI5 Theme**<br>sap_horizon|
|**UI5 Version**<br>1.114.9|
|**Enable TypeScript**<br>False|
|**Add Eslint configuration**<br>True, see https://www.npmjs.com/package/@sap-ux/eslint-plugin-fiori-tools#rules for the eslint rules.|
|**Main Entity**<br>ZCSSV_Sales_Analysis|

## project2

An SAP Fiori application.```text
┌─────────────────┐       JSON-RPC (Tool Call)       ┌─────────────────────┐
│  Agent / LLM    │ ───────────────────────────────> │     MCP Server      │
│  Orchestrator   │ <─────────────────────────────── │ (po-mcp/tools.py)   │
└─────────────────┘        Return PO Data Payload    └──────────┬──────────┘
                                                                │
                                                                │ CSV File Query
                                                                ▼
                                                     ┌─────────────────────┐
                                                     │     Data Source     │
                                                     │ (po-mcp/po_list.csv)│
                                                     └─────────────────────┘