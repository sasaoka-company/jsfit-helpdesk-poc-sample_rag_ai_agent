#!/usr/bin/env python3
"""
agent_core.pyの直接テスト
サーバーを介さずに直接動作確認
"""

import sys
import os
import time

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_core import create_agent, run_agent
from langchain_core.messages import HumanMessage
from logger import get_logger

logger = get_logger(__name__)


def test_direct_agent():
    """サーバーを介さない直接のエージェントテスト"""

    print("=== エージェント直接テスト開始 ===")

    try:
        # エージェント作成
        print("エージェントを作成中...")
        start_time = time.time()

        agent = create_agent()
        create_time = time.time() - start_time
        print(f"✅ エージェント作成完了: {create_time:.2f}秒")

        # 短い質問でテスト
        print("\n短い質問をテスト中...")
        query = "こんにちは"
        messages = [HumanMessage(content=query)]

        start_time = time.time()
        response = run_agent(agent, messages)
        response_time = time.time() - start_time

        print(f"✅ 応答完了: {response_time:.2f}秒")
        print(f"質問: {query}")
        print(f"回答: {response.content[:100]}...")

        return True

    except Exception as e:
        print(f"❌ エラー発生: {e}")
        logger.error(f"直接テストでエラー: {e}")
        return False


if __name__ == "__main__":
    success = test_direct_agent()
    if success:
        print("\n✅ 直接テスト成功 - 問題はサーバー設定にある可能性があります")
    else:
        print("\n❌ 直接テスト失敗 - エージェント自体に問題があります")
