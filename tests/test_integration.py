#!/usr/bin/env python3
"""
統合MCP クライアントのテストスクリプト
"""

from agent_core import create_agent, run_agent
from mcp_client_fastmcp import create_mcp_client_tools, SUPPORTED_TRANSPORTS


def test_integration():
    """
    統合テスト: 各トランスポート方式の基本動作確認
    """
    print("=== MCP クライアント統合テスト ===")
    print(f"サポート対象トランスポート: {SUPPORTED_TRANSPORTS}")
    print()

    for transport in SUPPORTED_TRANSPORTS:
        print(f"--- {transport.upper()} トランスポートテスト ---")

        try:
            if transport == "http":
                # HTTP方式の場合、明示的にserver_urlを指定
                tool = create_mcp_client_tools(
                    transport, server_url="http://127.0.0.1:8001/mcp"
                )
            else:
                tool = create_mcp_client_tools(transport)

            print(f"✓ {transport} ツール作成成功")
            print(f"  ツール名: {tool.name}")
            print(f"  説明: {tool.description}")

            # 実際のクエリテスト（接続エラーは想定内）
            try:
                result = tool.run("テストクエリ")
                print(f"  クエリ結果（抜粋）: {result[:100]}...")
            except Exception as e:
                if "接続エラー" in str(e) or "failed to connect" in str(e):
                    print(
                        f"  ✓ クエリテスト: 接続エラー（MCPサーバー未起動のため想定内）"
                    )
                else:
                    print(f"  ⚠ クエリテストエラー: {e}")

        except Exception as e:
            print(f"  ✗ {transport} ツール作成失敗: {e}")

        print()


def test_invalid_transport():
    """
    無効なトランスポート指定のテスト
    """
    print("--- 無効なトランスポート指定テスト ---")
    try:
        tool = create_mcp_client_tools("invalid_transport")
        print("✗ 無効なトランスポートが受け入れられました（想定外）")
    except ValueError as e:
        print(f"✓ 無効なトランスポートが適切に拒否されました: {e}")
    except Exception as e:
        print(f"⚠ 予期しないエラー: {e}")


if __name__ == "__main__":
    print("注意: このテストはMCPサーバーが起動していなくても実行可能です。")
    print("接続エラーは正常な動作として表示されます。")
    print()

    test_integration()
    test_invalid_transport()

    print("=== 統合テスト完了 ===")
