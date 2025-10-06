from mcp_client_fastmcp.http_client import create_http_mcp_tools

try:
    t = create_http_mcp_tools(http_server_url="http://127.0.0.1:8001/mcp")
    print("TOOL_NAME:", t.name)
    print("TOOL_DESC:", t.description)
except Exception as e:
    print("ERROR:", repr(e))
