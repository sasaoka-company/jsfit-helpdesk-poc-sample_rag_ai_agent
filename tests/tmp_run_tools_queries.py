from mcp_client_fastmcp import create_mcp_client_tools

print("Creating tools (server_url=http://127.0.0.1:8001/mcp)")
tools = create_mcp_client_tools(server_url="http://127.0.0.1:8001/mcp")

for i, tool in enumerate(tools, 1):
    print(
        f'--- Tool {i}: {tool.name} ({getattr(tool.func, "_mcp_meta", {}).get("transport")}) ---'
    )
    try:
        res = tool.run("テストクエリ")
        print("Result (excerpt):", res[:200])
    except Exception as e:
        print("Error running tool:", e)
    print()
