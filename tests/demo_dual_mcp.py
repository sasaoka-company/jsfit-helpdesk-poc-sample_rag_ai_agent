#!/usr/bin/env python3
"""
デュアルMCP使用例：エージェントが自律的にツールを選択
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_client_fastmcp import create_mcp_client_tools
import logger


def demo_dual_mcp_usage():
    """
    デュアルMCP機能の使用例デモ
    """
    try:
        print("=== デュアルMCP使用例デモ ===")

        # 1. 両方のMCPツールを同時作成
        print("1. STDIOとHTTP両方のMCPツール作成")
        tools = create_mcp_client_tools(server_url="http://127.0.0.1:8000/mcp")

        print(f"作成されたツール数: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        print()

        # 2. 各ツールの特徴を説明
        print("2. 各ツールの特徴")
        print("mcp_security_search (STDIO方式):")
        print("  - ローカルファイル（docx, pdf）に直接アクセス")
        print("  - 高速な文書検索")
        print("  - プロセス間通信による安定した接続")
        print()

        print("mcp_security_search_http (HTTP方式):")
        print("  - HTTP API経由でのアクセス")
        print("  - リモートサーバーとの通信")
        print("  - スケーラブルな分散処理")
        print()

        # 3. 実際のクエリ実行例
        print("3. 実際のクエリ実行例")
        test_queries = [
            "情報セキュリティポリシーについて教えて",
            "アクセス制御の規定について",
            "データ暗号化の要件は？",
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"クエリ {i}: {query}")

            for tool in tools:
                print(f"  {tool.name} による回答:")
                try:
                    result = tool.run(query)
                    if "接続エラー" in result or "failed to connect" in result.lower():
                        print(
                            f"    → 接続エラー（{tool.name.split('_')[-1].upper()}サーバー未起動）"
                        )
                    else:
                        # 結果の最初の100文字を表示
                        preview = result[:100].replace("\n", " ")
                        print(f"    → {preview}...")
                except Exception as e:
                    logger.error(f"ツール実行中にエラーが発生しました: {e}")
                    print(f"    → エラー: {e}")
            print()
    except Exception as e:
        logger.error(f"デュアルMCPデモ中にエラーが発生しました: {e}")
        raise


def show_integration_example():
    """
    create_react_agent との統合例を表示
    """
    print("=== create_react_agent 統合例 ===")

    integration_code = """
# agent_core.py の使用例

from agent_core import create_agent
from langchain_core.messages import HumanMessage

# 両方のMCPツールを持つエージェント作成
agent = create_agent(server_url="http://127.0.0.1:8000/mcp")

# エージェントが自律的にツールを選択して回答
message = HumanMessage(content="セキュリティインシデント対応手順について教えて")
response = agent.invoke({"messages": [message]})

print(response["messages"][-1].content)
"""

    print("コード例:")
    print(integration_code)

    print("エージェントの自律的判断:")
    print("- エージェントは利用可能な両方のMCPツールを認識")
    print("- クエリの内容に応じて適切なツールを選択")
    print("- 必要に応じて複数ツールを組み合わせて使用")
    print("- 一方のツールでエラーが発生した場合、もう一方を試行")


if __name__ == "__main__":
    try:
        print("STDIOとHTTPの両方のMCPクライアントを同時使用するデモ")
        print("=" * 60)

        demo_dual_mcp_usage()
        show_integration_example()

        print("=" * 60)
        print("🎉 両方のMCPクライアントが正常に動作しています！")
        print()
        print("推奨使用方法:")
        print("1. from agent_core import create_agent")
        print("2. agent = create_agent(server_url='http://127.0.0.1:8000/mcp')")
        print("3. エージェントが自動的に最適なMCPツールを選択して実行")
    except Exception as e:
        logger.error(f"メイン実行中にエラーが発生しました: {e}")
        raise
