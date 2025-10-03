# mcp_client/http_client.py
"""
MCPサーバーとのStreamable HTTP方式による連携を専門に扱うモジュール
FastMCPのClient(url)方式を使用してMCPサーバーに接続し、動的スキーマ対応のクライアント機能を提供
"""

import asyncio
from typing import Dict, Any, List
from langchain.tools import Tool
from fastmcp import Client
from logger import get_logger

# ロガー設定
logger = get_logger(__name__)

# MCPサーバー設定（HTTP方式用）
HTTP_SERVER_URL = "http://127.0.0.1:8001/mcp"  # デフォルトのHTTPサーバーURL
HTTP_TIMEOUT = 30  # タイムアウト設定（秒）


class HttpMCPClient:
    """
    Streamable HTTP方式のMCPクライアント
    FastMCPのClient(url)方式を使用してHTTP通信を行う
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        HTTP MCPクライアントの初期化

        Args:
            config: 設定辞書（Noneの場合はデフォルト設定を使用）
        """
        # デフォルト設定
        self.server_url = HTTP_SERVER_URL
        self.timeout = HTTP_TIMEOUT

        # カスタム設定があれば上書き
        if config:
            self.server_url = config.get("server_url", HTTP_SERVER_URL)
            self.timeout = config.get("timeout", HTTP_TIMEOUT)

        logger.info(f">>> MCPクライアント(HTTP)初期化完了: {self.server_url}")

    async def execute_query(self, query: str) -> str:
        """
        HTTP方式での専用クエリ実行

        Args:
            query: 検索クエリ

        Returns:
            MCPサーバーからの応答テキスト
        """
        logger.info(f">>> MCPサーバーへクエリ実行開始: {query}")
        logger.info(f">>> 接続先URL: {self.server_url}")

        try:
            # FastMCPのClient(url)方式でHTTP接続
            client = Client(self.server_url)

            async with client:
                logger.info(">>> MCPサーバーへの接続確立")

                # MCPサーバーから利用可能なツールを取得
                tools = await client.list_tools()
                logger.info(f">>> list_tools()の戻り値型: {type(tools)}")
                logger.info(f">>> list_tools()の内容: {tools}")

                # ツールリストの正規化
                tool_list = self._normalize_tool_list(tools)

                if not tool_list:
                    logger.warning(
                        ">>> MCPサーバーに利用可能なツールが見つかりませんでした"
                    )
                    return "MCPサーバーに利用可能なツールが見つかりませんでした。"

                # 最初のツールを使用
                first_tool = tool_list[0]
                tool_name = (
                    first_tool.name if hasattr(first_tool, "name") else str(first_tool)
                )
                logger.info(f">>> 使用するツール: {tool_name}")

                # 動的パラメータ判定
                arguments = self._build_arguments(first_tool, query)

                # ツール実行
                logger.info(f">>> ツール実行開始: {tool_name} with query: {query}")
                result = await client.call_tool(name=tool_name, arguments=arguments)
                logger.info(f">>> ツール実行完了: {tool_name}")

                # 応答処理
                response_text = self._extract_response_text(result)
                logger.info(
                    f">>> MCPサーバーからの応答取得成功 (文字数: {len(response_text)})"
                )
                return response_text

        except Exception as e:
            error_msg = f"MCPサーバーへの接続エラー: {str(e)}"
            logger.error(f">>> {error_msg}")
            return error_msg

    def _normalize_tool_list(self, tools) -> list:
        """
        ツールリストを正規化する

        Args:
            tools: MCPサーバーから返されたツール情報

        Returns:
            List[Any]: 正規化されたツールリスト
        """
        # tools が直接リストの場合とオブジェクトの場合を両方対応
        if hasattr(tools, "tools"):
            # tools.tools の形式の場合
            tool_list = tools.tools
        elif isinstance(tools, list):
            # tools が直接リストの場合
            tool_list = tools
        else:
            logger.error(f">>> 予期しないtools形式: {type(tools)}")
            return []

        if tool_list:
            tool_names = [
                tool.name if hasattr(tool, "name") else str(tool) for tool in tool_list
            ]
            logger.info(f">>> 利用可能なツール: {tool_names}")
        else:
            logger.info(">>> 利用可能なツール: なし")

        return tool_list

    def _build_arguments(self, tool, query: str) -> Dict[str, Any]:
        """
        ツールのスキーマから動的に引数を構築する

        Args:
            tool: MCPツールオブジェクト
            query: クエリ文字列

        Returns:
            Dict[str, Any]: ツール実行用の引数辞書
        """
        # MCPツールのスキーマから必要なパラメータを動的に取得
        input_schema = tool.inputSchema if hasattr(tool, "inputSchema") else {}
        required_params = input_schema.get("required", []) if input_schema else []
        properties = input_schema.get("properties", {}) if input_schema else {}

        # 適切な引数を構築
        arguments = {}
        if required_params:
            # 最初の必須パラメータにクエリを渡す（一般的なケース）
            first_param = required_params[0]
            arguments[first_param] = query
            logger.info(f">>> 使用するパラメータ: {first_param} = {query}")
        else:
            # フォールバック: 一般的なパラメータ名を試す
            common_params = ["query", "prompt", "input", "text", "question"]
            used_param = None
            for param in common_params:
                if param in properties:
                    arguments[param] = query
                    used_param = param
                    break

            if not used_param:
                # 最後の手段: プロパティの最初のものを使用
                if properties:
                    first_property = list(properties.keys())[0]
                    arguments[first_property] = query
                    used_param = first_property
                else:
                    logger.error(">>> ツールのスキーマ情報が不明です")
                    raise ValueError("MCPツールのスキーマ情報を取得できませんでした。")

            logger.info(f">>> 推定パラメータ: {used_param} = {query}")

        return arguments

    def _extract_response_text(self, result) -> str:
        """
        MCPサーバーからの応答をテキストに変換する

        Args:
            result: MCPサーバーからの応答オブジェクト

        Returns:
            str: 応答テキスト
        """
        if result.content:
            # テキストコンテンツを抽出
            text_content = []
            for content in result.content:
                if hasattr(content, "text"):
                    text_content.append(content.text)
                else:
                    text_content.append(str(content))
            return "\n".join(text_content)
        else:
            logger.warning(">>> MCPサーバーからの応答が空でした")
            return "MCPサーバーからの応答が空でした。"

    def query_sync(self, query: str) -> str:
        """
        同期的なクエリ実行

        Args:
            query: 検索クエリ

        Returns:
            MCPサーバーからの応答テキスト
        """
        return asyncio.run(self.execute_query(query))


# 従来の関数型インターフェース（後方互換性）
def http_mcp_query(query: str, server_url: str = None) -> str:
    """
    MCPサーバーにHTTP方式で接続してクエリを実行する（同期版）

    Args:
        query: 検索クエリ
        server_url: サーバーURL（Noneの場合はデフォルトを使用）

    Returns:
        MCPサーバーからの応答テキスト
    """
    config = None
    if server_url:
        config = {"server_url": server_url}

    client = HttpMCPClient(config)
    return client.query_sync(query)


async def get_http_mcp_tools_info(server_url: str) -> List[Dict[str, Any]]:
    """
    MCPサーバーから利用可能なツール情報を取得する（HTTP方式）

    Args:
        server_url: MCPサーバーのURL

    Returns:
        List[Dict]: ツール情報のリスト（name, description, inputSchemaを含む）
    """
    try:
        client = Client(server_url)

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
        # フォールバック：デフォルト情報を返す
        return [
            {
                "name": "mcp_security_search_http",
                "description": "セキュリティ関連の専門的な検索・分析を行うMCPサーバーツール（Streamable HTTP方式）",
                "inputSchema": {},
            }
        ]


def create_http_mcp_tools() -> List[Tool]:
    """
    MCPサーバーにStreamable HTTP方式で接続するツールを全て作成
    MCPサーバーから動的にツール情報を取得して複数のLangChainツールとして提供
    """
    # サーバーURLを直接使用
    final_server_url = HTTP_SERVER_URL

    try:
        # ツール情報を取得
        tools_info = asyncio.run(get_http_mcp_tools_info(final_server_url))

        if not tools_info:
            logger.warning(
                ">>> MCPサーバー（Streamable HTTP）からツール情報を取得できませんでした"
            )
            raise RuntimeError("MCPサーバー（Streamable HTTP）に接続できません")

        # 全てのツールをLangChain Toolとして作成
        langchain_tools: List[Tool] = []
        for tool_info in tools_info:
            tool_name = tool_info["name"]
            tool_description = tool_info["description"]

            # 説明にHTTP方式を追記（サーバが返すツール名は変更しない）
            if "http" not in tool_description.lower():
                tool_description = f"{tool_description}（Streamable HTTP方式）"

            # --- func に MCP メタ情報を付与 ---
            http_mcp_query._mcp_meta = {
                "transport": "http",
                "server_url": final_server_url,
                "tool_name": tool_name,
                "inputSchema": tool_info.get("inputSchema", {}),
            }

            langchain_tool = Tool(
                name=tool_name,
                description=tool_description,
                func=http_mcp_query,
            )
            langchain_tools.append(langchain_tool)

        logger.info(
            f">>> MCPクライアント(Streamable HTTP)ツール作成完了: {len(langchain_tools)}個のツール"
        )
        return langchain_tools

    except Exception as e:
        logger.error(f">>> HTTPツール作成エラー: {e}")
        raise
