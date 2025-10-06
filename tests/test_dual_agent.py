#!/usr/bin/env python3
"""
デュアルMCP（STDIO + HTTP）エージェントのテストスクリプト
"""

import asyncio
from langchain_core.messages import HumanMessage
from agent_core import create_agent, create_default_agent
from mcp_client_fastmcp import create_mcp_client_tools, create_dual_mcp_tools


def test_dual_mcp_tools():
    """
    デュアルMCPツール作成のテスト
    """
    print("=== デュアルMCPツール作成テスト ===")

    try:
        print("1. create_mcp_client_tools() テスト")
        tools = create_mcp_client_tools(server_url="http://127.0.0.1:8000/mcp")
        print(f"作成されたツール数: {len(tools)}")
        for i, tool in enumerate(tools):
            print(f"  ツール{i+1}: {tool.name} - {tool.description[:50]}...")
        print()

        print("2. create_dual_mcp_tools() テスト")
        dual_tools = create_dual_mcp_tools(
            http_config={"server_url": "http://127.0.0.1:8000/mcp"}
        )
        print(f"作成されたツール辞書: {list(dual_tools.keys())}")
        for transport, tool in dual_tools.items():
            if tool:
                print(f"  {transport}: {tool.name}")
            else:
                print(f"  {transport}: 作成失敗")
        print()

    except Exception as e:
        print(f"デュアルMCPツールテストでエラー: {e}")


def test_dual_agent_creation():
    """
    デュアルエージェント作成のテスト
    """
    print("=== デュアルエージェント作成テスト ===")

    try:
        print("1. create_agent() テスト（デュアルMCP対応）")
        dual_agent = create_agent(server_url="http://127.0.0.1:8000/mcp")
        print("✓ デュアルエージェント作成成功")

        print("2. create_agent() テスト（設定なし）")
        both_agent = create_agent()
        print("✓ デフォルト設定エージェント作成成功")

        print("3. 従来のデフォルトエージェント作成テスト")
        default_agent = create_default_agent()
        print("✓ デフォルトエージェント作成成功")

    except Exception as e:
        print(f"エージェント作成テストでエラー: {e}")


def test_agent_interaction():
    """
    エージェントとの対話テスト（簡単なメッセージ）
    """
    print("=== エージェント対話テスト ===")

    try:
        # デュアルエージェント作成
        agent = create_agent(server_url="http://127.0.0.1:8000/mcp")

        # 簡単なメッセージでテスト
        message = HumanMessage(content="利用可能なツールを教えて")
        print(f"送信メッセージ: {message.content}")

        print("注意: この対話テストは実際のMCPサーバーが必要です。")
        print("サーバー未起動の場合は接続エラーが発生します。")

        # 実際の対話はコメントアウト（サーバー未起動のため）
        # response = agent.invoke({"messages": [message]})
        # print(f"エージェント応答: {response}")

        print("✓ エージェント対話準備完了（実行はスキップ）")

    except Exception as e:
        print(f"エージェント対話テストでエラー: {e}")


if __name__ == "__main__":
    print("デュアルMCP（STDIO + HTTP）エージェントテスト開始")
    print(
        "注意: HTTPサーバーが http://127.0.0.1:8000/mcp で起動していることが理想ですが、"
    )
    print(
        "      サーバー未起動でもツール作成とエージェント作成のテストは実行できます。"
    )
    print()

    test_dual_mcp_tools()
    test_dual_agent_creation()
    test_agent_interaction()

    print("=== 全テスト完了 ===")
    print()
    print("使用方法:")
    print("from agent_core import create_agent")
    print("agent = create_agent(server_url='http://127.0.0.1:8000/mcp')")
    print("# これでSTDIOとStreamable HTTP両方のMCPツールを同時使用可能")
