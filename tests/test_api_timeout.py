#!/usr/bin/env python3
"""
タイムアウト設定のテスト用スクリプト
gpt-oss:20bモデルの長時間処理に対応したHTTPクライアント
"""

import requests
import time
import json
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_api_timeout():
    """API のタイムアウト設定をテスト"""

    url = "http://localhost:8000/query"
    headers = {"Content-Type": "application/json"}

    # 短い質問でテスト
    query_data = {"query": "こんにちは、調子はどうですか？"}

    print("=== 短い質問でのタイムアウトテスト ===")
    start_time = time.time()

    try:
        # 180秒のタイムアウト設定
        response = requests.post(
            url, headers=headers, json=query_data, timeout=180  # 3分のタイムアウト
        )

        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            print(f"✅ 成功: {elapsed_time:.2f}秒で応答")
            result = response.json()
            print(f"質問: {result['query']}")
            print(f"回答: {result['answer'][:100]}...")
        else:
            print(f"❌ HTTPエラー: {response.status_code}")
            print(f"エラー内容: {response.text}")

    except requests.exceptions.Timeout:
        elapsed_time = time.time() - start_time
        print(f"⏰ タイムアウト: {elapsed_time:.2f}秒後にタイムアウト")

    except requests.exceptions.RequestException as e:
        elapsed_time = time.time() - start_time
        print(f"❌ 接続エラー ({elapsed_time:.2f}秒後): {e}")


def test_long_query():
    """長い質問での大型モデルテスト"""

    url = "http://localhost:8000/query"
    headers = {"Content-Type": "application/json"}

    # 長い詳細な質問
    query_data = {
        "query": "人工知能技術の最新トレンドについて、機械学習、深層学習、自然言語処理、コンピュータビジョンの各分野における革新的な技術とその応用例を含めて、詳細に説明してください。"
    }

    print("\n=== 長い質問での大型モデルテスト ===")
    start_time = time.time()

    try:
        # 3分のタイムアウト設定
        response = requests.post(url, headers=headers, json=query_data, timeout=180)

        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            print(f"✅ 成功: {elapsed_time:.2f}秒で応答")
            result = response.json()
            print(f"質問: {result['query'][:50]}...")
            print(f"回答長: {len(result['answer'])}文字")
            print(f"回答先頭: {result['answer'][:200]}...")
        else:
            print(f"❌ HTTPエラー: {response.status_code}")
            print(f"エラー内容: {response.text}")

    except requests.exceptions.Timeout:
        elapsed_time = time.time() - start_time
        print(f"⏰ タイムアウト: {elapsed_time:.2f}秒後にタイムアウト")

    except requests.exceptions.RequestException as e:
        elapsed_time = time.time() - start_time
        print(f"❌ 接続エラー ({elapsed_time:.2f}秒後): {e}")


if __name__ == "__main__":
    print("大型モデル対応タイムアウト設定のテスト開始")
    print("サーバー: http://localhost:8000")
    print("クライアントタイムアウト: 180秒")
    print("サーバーKeep-alive: 300秒")

    # 短い質問でのテスト
    test_api_timeout()

    # 少し待機
    time.sleep(2)

    # 長い質問でのテスト
    test_long_query()

    print("\nテスト完了")
