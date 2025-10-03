"""ログローテーション機能のテスト"""

import os
import sys
import time
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import get_logger


def test_logger_rotation():
    """ログローテーション機能のテスト"""
    print("ログローテーション機能のテストを開始...")

    # ロガーを取得
    logger = get_logger("test_logger")

    # 現在の日時を記録
    current_time = datetime.now()
    print(f"テスト開始時刻: {current_time}")

    # テストログを出力
    for i in range(5):
        logger.info(f"テストログメッセージ {i+1}: {current_time}")
        time.sleep(0.1)

    # ログディレクトリの確認
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log"
    )
    if os.path.exists(log_dir):
        log_files = os.listdir(log_dir)
        print(f"\nログディレクトリ内のファイル: {log_files}")

        # app.logファイルの内容を確認
        app_log_path = os.path.join(log_dir, "app.log")
        if os.path.exists(app_log_path):
            print(f"\napp.logファイルサイズ: {os.path.getsize(app_log_path)} bytes")
            print("app.logの最新5行:")
            with open(app_log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-5:]:
                    print(f"  {line.strip()}")

    print("\nログローテーション設定:")
    handler = logger.handlers[0] if logger.handlers else None
    if handler and hasattr(handler, "when"):
        print(f"  ローテーション間隔: {handler.when}")
        print(f"  バックアップ保持数: {handler.backupCount}")
        print(f"  ファイル名サフィックス: {handler.suffix}")

    print("\nテスト完了!")


if __name__ == "__main__":
    test_logger_rotation()
