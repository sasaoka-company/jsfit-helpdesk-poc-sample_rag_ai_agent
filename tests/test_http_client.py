#!/usr/bin/env python3
"""
HTTP MCPクライアントのテストスクリプト
"""

import asyncio
import time

from mcp_client_fastmcp.http_client import (
    HttpMCPClient,
    http_mcp_query,
    create_http_mcp_tools,
)


async def test_http_mcp_client():
    """
    HTTP MCPクライアントの基本テスト
    """
    print("=== HTTP MCPクライアント テスト開始 ===")

    # 設定をユーザー指定のサーバーに合わせて調整
    config = {"server_url": "http://127.0.0.1:8001/mcp"}  # デフォルト設定を使用

    client = HttpMCPClient(config)

    try:
        print("1. 非同期クエリテスト")
        result = await client.execute_query("セキュリティポリシーについて教えて")
        print(f"結果: {result}")
        print()

        print("2. 同期クエリテスト（別プロセスで実行）")
        # 注意: 既に非同期コンテキスト内なので、同期版は別途テスト
        print("同期テストは関数型インターフェースでテストします")
        print()

    except Exception as e:
        print(f"テスト中にエラーが発生しました: {e}")


def test_function_interface():
    """
    関数型インターフェースのテスト（同期実行）
    """
    print("3. 関数型インターフェーステスト")
    try:
        result = http_mcp_query("アクセス制御について")
        print(f"結果: {result}")
        print()
    except Exception as e:
        print(f"関数型インターフェーステスト中にエラーが発生しました: {e}")


def test_langchain_tool():
    """
    LangChainツール形式のテスト（同期実行）
    """
    print("4. LangChainツール形式テスト")
    try:
        tool = create_http_mcp_tools()
        result = tool.run("データ暗号化について")
        print(f"結果: {result}")
        print()
    except Exception as e:
        print(f"LangChainツールテスト中にエラーが発生しました: {e}")


async def main():
    """
    メイン実行関数
    """
    print(
        "HTTP MCPサーバーが http://127.0.0.1:8001/mcp で起動していることを確認してください。"
    )
    print()

    # 非同期テスト
    await test_http_mcp_client()

    # 同期テスト（新しいイベントループで実行）
    test_function_interface()
    test_langchain_tool()

    print("=== テスト完了 ===")


if __name__ == "__main__":
    asyncio.run(main())
