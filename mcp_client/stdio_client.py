# mcp_client/stdio_client.py
"""
MCPサーバーとの標準入出力方式による連携を専門に扱うモジュール
PythonStdioTransportを使用してMCPサーバーに接続し、動的スキーマ対応のクライアント機能を提供
"""

import asyncio
from functools import lru_cache
from typing import Dict, Any, List
from langchain.tools import Tool
from fastmcp.client.transports import PythonStdioTransport
from fastmcp import Client
from .base_client import BaseMCPClient
from logger import get_logger

# ロガー設定
logger = get_logger(__name__)

# MCPサーバー設定（標準入出力方式用）
STDIO_PYTHON_EXECUTABLE = (
    "D:\\vscode_projects\\sample_rag_mcp_server_stdio\\.venv\\Scripts\\python.exe"
)
STDIO_SERVER_SCRIPT = (
    "D:\\vscode_projects\\sample_rag_mcp_server_stdio\\rag_mcp_server_stdio.py"
)


class StdioMCPClient(BaseMCPClient):
    """
    標準入出力方式のMCPクライアント
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        標準入出力MCPクライアントの初期化

        Args:
            config: 設定辞書（Noneの場合はデフォルト設定を使用）
        """
        if config is None:
            config = {
                "python_executable": STDIO_PYTHON_EXECUTABLE,
                "server_script": STDIO_SERVER_SCRIPT,
            }
        super().__init__(config)
        logger.info(">>> MCPクライアント(STDIO)初期化完了")

    async def create_transport(self):
        """
        PythonStdioTransportを作成する

        Returns:
            PythonStdioTransport: 標準入出力方式のトランスポート
        """
        return PythonStdioTransport(
            script_path=self.config["server_script"],
            python_cmd=self.config["python_executable"],
        )

    async def execute_query(self, query: str) -> str:
        """
        標準入出力方式での専用クエリ実行

        Args:
            query: 検索クエリ

        Returns:
            MCPサーバーからの応答テキスト
        """
        # 基底クラスの共通処理を実行（ログは基底クラスで出力される）
        result = await super().execute_query(query)
        logger.info(">>> MCPクライアント(STDIO)処理完了")
        return result


# 従来の関数型インターフェース（後方互換性）
def stdio_mcp_query(query: str) -> str:
    """
    MCPサーバーに標準入出力方式で接続してクエリを実行する（同期版）

    Args:
        query: 検索クエリ

    Returns:
        MCPサーバーからの応答テキスト
    """
    client = StdioMCPClient()
    return client.query_sync(query)


async def get_stdio_mcp_tools_info() -> List[Dict[str, Any]]:
    """
    MCPサーバーから利用可能なツール情報を取得する

    Returns:
        List[Dict]: ツール情報のリスト（name, description, inputSchemaを含む）
    """
    try:
        transport = PythonStdioTransport(
            script_path=STDIO_SERVER_SCRIPT,
            python_cmd=STDIO_PYTHON_EXECUTABLE,
        )

        client = Client(transport=transport)

        async with client:
            # 利用可能なツールを取得
            tools = await client.list_tools()

            # ツールリストを正規化
            if hasattr(tools, "tools"):
                tool_list = tools.tools
            elif isinstance(tools, list):
                tool_list = tools
            else:
                error_msg = f"予期しないtools形式: {type(tools)}"
                logger.error(f">>> {error_msg}")
                raise ValueError(error_msg)

            # ツール情報を辞書形式で収集
            tools_info = []
            for tool in tool_list:
                tool_info = {
                    "name": getattr(tool, "name", "unknown_tool"),
                    "description": getattr(
                        tool, "description", "MCPサーバーから提供されるツール"
                    ),
                    "inputSchema": getattr(tool, "inputSchema", {}),
                }
                tools_info.append(tool_info)
                logger.info(
                    f">>> 検出されたツール: {tool_info['name']} - {tool_info['description']}"
                )

            return tools_info

    except Exception as e:
        logger.error(f">>> MCPサーバーからのツール情報取得エラー: {e}")
        return []


def create_stdio_mcp_tools() -> List[Tool]:
    """
    MCPサーバーに標準入出力方式で接続するツールを全て作成
    MCPサーバーから動的にツール情報を取得して複数のLangChainツールとして提供
    """
    try:
        # ツール情報を取得
        tools_info = asyncio.run(get_stdio_mcp_tools_info())

        if not tools_info:
            logger.warning(
                ">>> MCPサーバー（STDIO）からツール情報を取得できませんでした"
            )
            raise RuntimeError("MCPサーバー（STDIO）に接続できません")

        # 全てのツールをLangChain Toolとして作成
        langchain_tools: List[Tool] = []
        for tool_info in tools_info:
            tool_name = tool_info["name"]
            tool_description = tool_info["description"]

            # 説明に通信方式を追記（サーバが返すツール名は変更しない）
            if "標準入出力方式" not in tool_description:
                tool_description = f"{tool_description}（標準入出力方式）"

            # --- func に MCP メタ情報を付与 ---
            stdio_mcp_query._mcp_meta = {
                "transport": "stdio",
                "server_script": STDIO_SERVER_SCRIPT,
                "python_executable": STDIO_PYTHON_EXECUTABLE,
                "tool_name": tool_name,
                "inputSchema": tool_info.get("inputSchema", {}),
            }

            langchain_tool = Tool(
                name=tool_name,
                description=tool_description,
                func=stdio_mcp_query,
            )
            langchain_tools.append(langchain_tool)

        logger.info(
            f">>> MCPクライアント(STDIO)ツール初期化完了: {len(langchain_tools)}個のツール"
        )
        return langchain_tools

    except Exception as e:
        logger.error(f">>> STDIOツール作成エラー: {e}")
        raise
