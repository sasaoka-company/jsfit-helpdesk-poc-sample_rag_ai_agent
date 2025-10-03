from agent_core import create_agent

print("Creating dual agent with HTTP server on port 8001")
agent = create_agent(server_url="http://127.0.0.1:8001/mcp")

# ツール一覧を確認
print(f"Agent tools count: {len(agent.tools)}")
for i, tool in enumerate(agent.tools, 1):
    print(f"Tool {i}: {tool.name} - {tool.description[:60]}...")
    if hasattr(tool, "func") and hasattr(tool.func, "_mcp_meta"):
        print(f'  Transport: {tool.func._mcp_meta.get("transport")}')
