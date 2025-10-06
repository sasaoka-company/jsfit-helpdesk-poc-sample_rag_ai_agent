import sys
import traceback
import asyncio

from mcp_client_fastmcp.http_client import HttpMCPClient

try:
    print("Initializing HttpMCPClient with server_url=http://127.0.0.1:8001/mcp")
    client = HttpMCPClient({"server_url": "http://127.0.0.1:8001/mcp"})
    print("Calling query_sync...")
    res = client.query_sync("テスト")
    print("=== RESULT ===")
    print(res)
except Exception as e:
    print("Exception during test:")
    traceback.print_exc()
    sys.exit(1)
else:
    sys.exit(0)
