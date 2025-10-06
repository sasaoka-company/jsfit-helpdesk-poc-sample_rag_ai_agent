from mcp_client_fastmcp.stdio_client import create_stdio_mcp_tools
from mcp_client_fastmcp.http_client import create_http_mcp_tools

s = create_stdio_mcp_tools()
print("STDIO ->", s.name, "|", s.description)

h = create_http_mcp_tools(http_server_url="http://127.0.0.1:8000/mcp")
print("HTTP  ->", h.name, "|", h.description)
