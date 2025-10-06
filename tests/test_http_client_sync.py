#!/usr/bin/env python3
"""
HTTP MCPクライアントの同期テストスクリプト
"""

from mcp_client_fastmcp.http_client import http_mcp_query, create_http_mcp_tools


def test_function_interface():
    """
    関数型インターフェースのテスト（同期実行）
    """
    print("=== 関数型インターフェーステスト ===")
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
    print("=== LangChainツール形式テスト ===")
    try:
        tool = create_http_mcp_tools()
        result = tool.run("データ暗号化について")
        print(f"結果: {result}")
        print()
    except Exception as e:
        print(f"LangChainツールテスト中にエラーが発生しました: {e}")


if __name__ == "__main__":
    print(
        "HTTP MCPサーバーが http://127.0.0.1:8001/mcp で起動していることを確認してください。"
    )
    print()

    # 同期テスト
    test_function_interface()
    test_langchain_tool()

    print("=== 同期テスト完了 ===")
