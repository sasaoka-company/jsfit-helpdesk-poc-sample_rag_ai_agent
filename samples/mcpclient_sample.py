import asyncio
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport


async def main():
    server_script = (
        "D:\\vscode_projects\\sample_rag_mcp_server_stdio\\rag_mcp_server.py"
    )

    transport = PythonStdioTransport(script_path=server_script)

    async with Client(transport=transport) as client:
        tools = await client.list_tools()
        print("ツール一覧:", tools)

        result = await client.call_tool("greet", {"name": "Alice"})
        print("greet ツールの結果:", result)


if __name__ == "__main__":
    asyncio.run(main())
