#!/usr/bin/env python3
"""
MCPクライアントのテストスクリプト
"""

import sys
import traceback


def test_imports():
    """インポートをテスト"""
    print("=== インポートテスト ===")
    try:
        from mcp_client_fastmcp.mcp_tools_factory import create_mcp_tools

        print("✓ mcp_tools_factory モジュールのインポート成功")

        from mcp_client_fastmcp.stdio_client import create_stdio_mcp_tools

        print("✓ stdio_client モジュールのインポート成功")

        from mcp_client_fastmcp.http_client import create_http_mcp_tools

        print("✓ http_client モジュールのインポート成功")

        return True
    except Exception as e:
        print(f"✗ インポートエラー: {e}")
        traceback.print_exc()
        return False


def test_stdio_tools():
    """STDIOツールの作成をテスト"""
    print("\n=== STDIOツール作成テスト ===")
    try:
        from mcp_client_fastmcp.stdio_client import create_stdio_mcp_tools

        tools = create_stdio_mcp_tools()
        print(f"✓ STDIOツール作成成功: {len(tools)}個のツール")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        return True
    except Exception as e:
        print(f"✗ STDIOツール作成エラー: {e}")
        traceback.print_exc()
        return False


def test_http_tools():
    """HTTPツールの作成をテスト"""
    print("\n=== HTTPツール作成テスト ===")
    try:
        from mcp_client_fastmcp.http_client import create_http_mcp_tools

        tools = create_http_mcp_tools()
        print(f"✓ HTTPツール作成成功: {len(tools)}個のツール")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        return True
    except Exception as e:
        print(f"✗ HTTPツール作成エラー: {e}")
        traceback.print_exc()
        return False


def test_dual_tools():
    """デュアルツールの作成をテスト"""
    print("\n=== デュアルツール作成テスト ===")
    try:
        from mcp_client_fastmcp import create_mcp_tools

        tools = create_mcp_tools()
        print(f"✓ デュアルツール作成成功: {len(tools)}個のツール")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        return True
    except Exception as e:
        print(f"✗ デュアルツール作成エラー: {e}")
        traceback.print_exc()
        return False


def main():
    """メイン関数"""
    print("MCPクライアントテスト開始")
    print(f"Python実行環境: {sys.executable}")

    # テスト実行
    tests = [
        ("インポート", test_imports),
        ("STDIO", test_stdio_tools),
        ("HTTP", test_http_tools),
        ("デュアル", test_dual_tools),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name}テスト例外: {e}")
            traceback.print_exc()
            results[test_name] = False

    # 結果サマリー
    print("\n=== テスト結果サマリー ===")
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")

    # 全体結果
    all_passed = all(results.values())
    print(f"\n全体結果: {'✓ ALL PASS' if all_passed else '✗ SOME FAILED'}")
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
