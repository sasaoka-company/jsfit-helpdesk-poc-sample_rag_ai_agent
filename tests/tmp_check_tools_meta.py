from mcp_client_fastmcp.http_client import create_http_mcp_tools
from mcp_client_fastmcp import create_mcp_client_tools

print("Testing create_http_mcp_client_tool (explicit server_url=8001)")
try:
    t = create_http_mcp_tools(http_server_url="http://127.0.0.1:8001/mcp")
    print("TOOL NAME:", t.name)
    print("DESC:", t.description)
    meta = getattr(t.func, "_mcp_meta", None)
    print("META:", meta)
except Exception as e:
    print("ERROR creating http tool:", e)

print("\nTesting create_mcp_client_tools (server_url=8001)")
try:
    tools = create_mcp_client_tools(server_url="http://127.0.0.1:8001/mcp")
    for i, tool in enumerate(tools, 1):
        print(f"--- Tool {i} ---")
        print("NAME:", tool.name)
        print("DESC:", tool.description)
        print("META:", getattr(tool.func, "_mcp_meta", None))
except Exception as e:
    print("ERROR creating all tools:", e)
