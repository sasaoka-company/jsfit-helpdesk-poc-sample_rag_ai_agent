#!/usr/bin/env python3
"""
MCPクライアント機能の基本テストスクリプト（依存関係最小版）
"""

import sys
import os

# パス追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mcp_client_fastmcp import (
        create_mcp_client_tools,
        create_dual_mcp_tools,
        SUPPORTED_TRANSPORTS,
    )
except ImportError as e:
    print(f"MCP クライアントモジュールのインポートエラー: {e}")
    sys.exit(1)


def test_dual_mcp_tools_basic():
    """
    デュアルMCPツール作成の基本テスト
    """
    print("=== デュアルMCPツール基本テスト ===")
    print(f"サポート対象トランスポート: {SUPPORTED_TRANSPORTS}")
    print()

    try:
        print("1. create_mcp_client_tools() テスト")
        tools = create_mcp_client_tools(server_url="http://127.0.0.1:8000/mcp")
        print(f"作成されたツール数: {len(tools)}")
        for i, tool in enumerate(tools):
            print(f"  ツール{i+1}: {tool.name}")
            print(f"    説明: {tool.description[:80]}...")
        print()

    except Exception as e:
        print(f"create_mcp_client_tools テストでエラー: {e}")
        import traceback

        traceback.print_exc()
        print()

    try:
        print("2. create_dual_mcp_tools() テスト")
        dual_tools = create_dual_mcp_tools(
            http_config={"server_url": "http://127.0.0.1:8000/mcp"}
        )
        print(f"作成されたツール辞書キー: {list(dual_tools.keys())}")
        for transport, tool in dual_tools.items():
            if tool:
                print(f"  {transport}: {tool.name} ✓")
            else:
                print(f"  {transport}: 作成失敗 ✗")
        print()

    except Exception as e:
        print(f"create_dual_mcp_tools テストでエラー: {e}")
        import traceback

        traceback.print_exc()
        print()


def test_individual_tools():
    """
    各ツールの個別テスト
    """
    print("=== 個別ツールテスト ===")

    try:
        from mcp_client_fastmcp.stdio_client import create_stdio_mcp_tools

        print("1. STDIOツール作成テスト")
        stdio_tool = create_stdio_mcp_tools()
        print(f"  STDIOツール: {stdio_tool.name} ✓")
    except Exception as e:
        print(f"  STDIOツール作成エラー: {e}")

    try:
        from mcp_client_fastmcp.http_client import create_http_mcp_tools

        print("2. HTTPツール作成テスト")
        http_tool = create_http_mcp_tools(http_server_url="http://127.0.0.1:8000/mcp")
        print(f"  HTTPツール: {http_tool.name} ✓")
    except Exception as e:
        print(f"  HTTPツール作成エラー: {e}")

    print()


def test_tool_functionality():
    """
    ツールの実際の機能テスト（接続テスト）
    """
    print("=== ツール機能テスト ===")
    print("注意: MCPサーバーが起動していない場合、接続エラーが発生します。")

    try:
        tools = create_mcp_client_tools(server_url="http://127.0.0.1:8000/mcp")

        for i, tool in enumerate(tools):
            print(f"{i+1}. {tool.name} 実行テスト")
            try:
                result = tool.run("テスト用クエリ")
                if "接続エラー" in result or "failed to connect" in result.lower():
                    print(f"  → 接続エラー（MCPサーバー未起動のため想定内）")
                else:
                    print(f"  → 成功: {result[:50]}...")
            except Exception as e:
                print(f"  → エラー: {e}")
        print()

    except Exception as e:
        print(f"ツール機能テストでエラー: {e}")


if __name__ == "__main__":
    print("=== MCPクライアント デュアル機能テスト ===")
    print("このテストでは以下を確認します:")
    print("- 複数のMCPツールの同時作成")
    print("- STDIOとHTTPツールの個別作成")
    print("- 各ツールの基本動作（接続テスト）")
    print()

    test_dual_mcp_tools_basic()
    test_individual_tools()
    test_tool_functionality()

    print("=== テスト完了 ===")
    print()
    print("推奨使用方法:")
    print("```python")
    print("from mcp_client import create_mcp_client_tools")
    print("tools = create_mcp_client_tools(server_url='http://127.0.0.1:8000/mcp')")
    print("# STDIOとHTTP両方のMCPツールが作成され、エージェントが自律的に選択可能")
    print("```")
