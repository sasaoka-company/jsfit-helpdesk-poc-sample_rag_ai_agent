import logging
import logging.handlers
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # このファイルのある場所
LOG_DIR = os.path.join(BASE_DIR, "log")

# 日時とプロセスIDを含むログファイル名で、ソート可能かつプロセス間競合を回避
PROCESS_ID = os.getpid()
START_TIME = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOG_DIR, f"app_{START_TIME}_pid{PROCESS_ID}.log")

os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # 既にハンドラが設定されている場合は再設定せず、そのまま返す
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # サイズベースのローテーションハンドラーを使用（複数プロセス対応）
    # プロセス毎に独立したログファイルを使用して競合を完全に回避
    fh = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # プロセス毎なので5ファイル分で十分
        encoding="utf-8",
        delay=True,  # ファイル作成を遅延させて競合を軽減
    )
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    # 親ロガーに伝播しないようにして重複を防ぐ
    logger.propagate = False

    return logger
