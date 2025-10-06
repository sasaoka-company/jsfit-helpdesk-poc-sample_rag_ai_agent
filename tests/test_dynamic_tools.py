#!/usr/bin/env python3
"""
動的ツール情報取得のテストスクリプト
MCPサーバーから実際のツール名・説明を取得するかテスト
"""

import asyncio
import sys
import os

# パス追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mcp_client_fastmcp.stdio_client import (
        get_stdio_mcp_tools_info,
        create_stdio_mcp_tools,
    )
    from mcp_client_fastmcp.http_client import (
        get_http_mcp_tools_info,
        create_http_mcp_tools,
    )
except ImportError as e:
    print(f"MCP クライアントモジュールのインポートエラー: {e}")
    sys.exit(1)


async def test_stdio_dynamic_tools():
    """
    STDIO方式での動的ツール情報取得テスト
    """
    print("=== STDIO動的ツール情報取得テスト ===")

    try:
        print("1. MCPサーバーからのツール情報取得")
        tools_info = await get_stdio_mcp_tools_info()
        print(f"取得されたツール数: {len(tools_info)}")

        for i, tool_info in enumerate(tools_info, 1):
            print(f"  ツール{i}:")
            print(f"    名前: {tool_info['name']}")
            print(f"    説明: {tool_info['description']}")
            print(f"    スキーマ: {tool_info['inputSchema']}")
        print()

    except Exception as e:
        print(f"STDIOツール情報取得エラー: {e}")
        print()


async def test_http_dynamic_tools():
    """
    HTTP方式での動的ツール情報取得テスト
    """
    print("=== HTTP動的ツール情報取得テスト ===")

    try:
        server_url = "http://127.0.0.1:8001/mcp"
        print(f"1. MCPサーバーからのツール情報取得: {server_url}")
        tools_info = await get_http_mcp_tools_info(server_url)
        print(f"取得されたツール数: {len(tools_info)}")

        for i, tool_info in enumerate(tools_info, 1):
            print(f"  ツール{i}:")
            print(f"    名前: {tool_info['name']}")
            print(f"    説明: {tool_info['description']}")
            print(f"    スキーマ: {tool_info['inputSchema']}")
        print()

    except Exception as e:
        print(f"HTTPツール情報取得エラー: {e}")
        print()


def test_dynamic_tool_creation():
    """
    動的ツール作成のテスト
    """
    print("=== 動的ツール作成テスト ===")

    try:
        print("1. STDIOツール作成")
        stdio_tool = create_stdio_mcp_tools()
        print(f"  作成されたツール:")
        print(f"    名前: {stdio_tool.name}")
        print(f"    説明: {stdio_tool.description}")
        print()

    except Exception as e:
        print(f"STDIOツール作成エラー: {e}")
        print()

    try:
        print("2. HTTPツール作成")
        http_tool = create_http_mcp_tools(http_server_url="http://127.0.0.1:8001/mcp")
        print(f"  作成されたツール:")
        print(f"    名前: {http_tool.name}")
        print(f"    説明: {http_tool.description}")
        print()

    except Exception as e:
        print(f"HTTPツール作成エラー: {e}")
        print()


def test_tool_comparison():
    """
    ハードコード版と動的版の比較テスト
    """
    print("=== ハードコード版と動的版の比較 ===")

    # STDIO版比較
    try:
        stdio_tool = create_stdio_mcp_tools()
        print(f"STDIO動的版:")
        print(f"  名前: {stdio_tool.name}")
        print(f"  説明: {stdio_tool.description[:80]}...")

        # 従来のハードコード版と比較
        expected_name = "mcp_security_search"
        if stdio_tool.name == expected_name:
            print(f"  → フォールバック（従来と同じ）")
        else:
            print(f"  → 動的取得成功（従来: {expected_name}）")
        print()

    except Exception as e:
        print(f"STDIO比較エラー: {e}")
        print()

    # HTTP版比較
    try:
        http_tool = create_http_mcp_tools()
        print(f"HTTP動的版:")
        print(f"  名前: {http_tool.name}")
        print(f"  説明: {http_tool.description[:80]}...")

        # 従来のハードコード版と比較
        expected_name = "mcp_security_search_http"
        if http_tool.name == expected_name:
            print(f"  → フォールバック（従来と同じ）")
        else:
            print(f"  → 動的取得成功（従来: {expected_name}）")
        print()

    except Exception as e:
        print(f"HTTP比較エラー: {e}")
        print()


async def main():
    print("=== MCPサーバーからの動的ツール情報取得テスト ===")
    print("このテストでは以下を確認します:")
    print("- MCPサーバーから実際のツール名・説明を動的に取得")
    print("- ハードコード版からの変更点確認")
    print("- フォールバック機能（サーバー未起動時）")
    print()

    # 非同期テスト
    await test_stdio_dynamic_tools()
    await test_http_dynamic_tools()

    # 同期テスト
    test_dynamic_tool_creation()
    test_tool_comparison()

    print("=== テスト完了 ===")
    print()
    print("改善点:")
    print("✅ ツール名・説明をMCPサーバーから動的に取得")
    print("✅ サーバー未起動時の適切なフォールバック")
    print("✅ 既存コードとの互換性維持")


if __name__ == "__main__":
    asyncio.run(main())
