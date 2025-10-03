from mcp_client import create_mcp_client_tools

tools = create_mcp_client_tools()
for t in tools:
    meta = getattr(t.func, "_mcp_meta", None)
    print("TOOL:", t.name)
    print("  desc:", t.description)
    print("  meta:", meta)
