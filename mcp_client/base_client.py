# mcp_client/base_client.py
"""
MCPクライアント基底クラス
通信方式に依存しない共通ロジックを提供
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from logger import get_logger

logger = get_logger(__name__)


class BaseMCPClient(ABC):
    """
    MCPクライアントの基底クラス
    通信方式に依存しない共通機能を提供
    """

    def __init__(self, config: Dict[str, Any]):
        """
        基底クライアントの初期化

        Args:
            config: 通信方式固有の設定辞書
        """
        self.config = config
        self.logger = logger

    @abstractmethod
    async def create_transport(self):
        """
        通信トランスポートを作成する（各サブクラスで実装）

        Returns:
            Transport: FastMCP互換のトランスポートオブジェクト
        """
        pass

    async def execute_query(self, query: str) -> str:
        """
        MCPサーバーへのクエリ実行（共通ロジック）

        Args:
            query: 検索クエリ

        Returns:
            MCPサーバーからの応答テキスト
        """
        self.logger.info(f">>> MCPサーバーへクエリ実行開始: {query}")

        try:
            transport = await self.create_transport()

            from fastmcp import Client

            async with Client(transport=transport) as client:
                self.logger.info(">>> MCPサーバーへの接続確立")

                # MCPサーバーから利用可能なツールを取得
                tools = await client.list_tools()
                self.logger.info(f">>> list_tools()の戻り値型: {type(tools)}")
                self.logger.info(f">>> list_tools()の内容: {tools}")

                # ツールリストの正規化
                tool_list = self._normalize_tool_list(tools)

                if not tool_list:
                    self.logger.warning(
                        ">>> MCPサーバーに利用可能なツールが見つかりませんでした"
                    )
                    return "MCPサーバーに利用可能なツールが見つかりませんでした。"

                # 最初のツールを使用
                first_tool = tool_list[0]
                tool_name = (
                    first_tool.name if hasattr(first_tool, "name") else str(first_tool)
                )
                self.logger.info(f">>> 使用するツール: {tool_name}")

                # 動的パラメータ判定
                arguments = self._build_arguments(first_tool, query)

                # ツール実行
                self.logger.info(f">>> ツール実行開始: {tool_name} クエリ： {query}")
                result = await client.call_tool(name=tool_name, arguments=arguments)
                self.logger.info(f">>> ツール実行完了: {tool_name}")

                # 応答処理
                response_text = self._extract_response_text(result)
                self.logger.info(
                    f">>> MCPサーバーからの応答取得成功 (文字数： {len(response_text)})"
                )
                self.logger.info(f">>> MCPサーバーからの応答： ({response_text})")
                return response_text

        except Exception as e:
            error_msg = f"MCPサーバーへの接続エラー: {str(e)}"
            self.logger.error(f">>> {error_msg}")
            return error_msg

    def _normalize_tool_list(self, tools) -> List[Any]:
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
            self.logger.error(f">>> 予期しないtools形式: {type(tools)}")
            return []

        if tool_list:
            tool_names = [
                tool.name if hasattr(tool, "name") else str(tool) for tool in tool_list
            ]
            self.logger.info(f">>> 利用可能なツール: {tool_names}")
        else:
            self.logger.info(">>> 利用可能なツール: なし")

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
            self.logger.info(f">>> 使用するパラメータ: {first_param} = {query}")
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
                    self.logger.error(">>> ツールのスキーマ情報が不明です")
                    raise ValueError("MCPツールのスキーマ情報を取得できませんでした。")

            self.logger.info(f">>> 推定パラメータ: {used_param} = {query}")

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
            self.logger.warning(">>> MCPサーバーからの応答が空でした")
            return "MCPサーバーからの応答が空でした。"

    def query_sync(self, query: str) -> str:
        """
        同期的なクエリ実行（共通ロジック）

        Args:
            query: 検索クエリ

        Returns:
            MCPサーバーからの応答テキスト
        """
        return asyncio.run(self.execute_query(query))
