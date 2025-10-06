from typing import List
from langchain_core.tools import Tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import STDIO_PYTHON_EXECUTABLE, STDIO_SERVER_SCRIPT, HTTP_SERVER_URL
from logger import get_logger

logger = get_logger(__name__)


async def create_mcp_tools() -> List[Tool]:
    logger.info(">>> MCP ツール作成開始（langchain-mcp-adapters使用）")

    # 複数のサーバへの接続を定義（公式ドキュメントの形式に合わせて修正）
    server_connections = {
        "search_security": {
            "command": STDIO_PYTHON_EXECUTABLE,
            "args": [STDIO_SERVER_SCRIPT],
            "transport": "stdio",
        },
        "search_work_rules": {
            "url": HTTP_SERVER_URL,
            "transport": "streamable_http",
        },
    }

    logger.info(f">>> サーバー接続設定: {server_connections}")
    logger.info(f">>> STDIO_PYTHON_EXECUTABLE: {STDIO_PYTHON_EXECUTABLE}")
    logger.info(f">>> STDIO_SERVER_SCRIPT: {STDIO_SERVER_SCRIPT}")
    logger.info(f">>> HTTP_SERVER_URL: {HTTP_SERVER_URL}")

    try:
        # MultiServerMCPClientのインスタンスを作成（正しい引数形式）
        logger.info(">>> MultiServerMCPClient インスタンス作成中...")
        client = MultiServerMCPClient(server_connections)
        logger.info(">>> MultiServerMCPClient インスタンス作成完了")

        # ツールを取得
        logger.info(">>> ツール取得開始...")
        tools = await client.get_tools()
        logger.info(f">>> ツール取得完了: {len(tools)}個のツールを取得")

        # 取得したツールの詳細をログ出力
        for i, tool in enumerate(tools):
            logger.info(f">>> ツール{i+1}: {tool.name} - {tool.description}")

        logger.info(">>> MCP ツール作成完了（langchain-mcp-adapters使用）")
        return tools

    except Exception as e:
        logger.error(f">>> MCP ツール作成エラー（langchain-mcp-adapters使用）: {e}")
        logger.error(f">>> エラー詳細: {type(e).__name__}: {str(e)}")
        raise
