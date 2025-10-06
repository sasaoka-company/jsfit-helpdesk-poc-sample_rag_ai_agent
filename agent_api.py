# agent_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent_core import create_agent, run_agent
from logger import get_logger
import time

# ロガー設定
logger = get_logger(__name__)

app = FastAPI(title="AIエージェントサーバー")

# エージェントインスタンスを遅延初期化（None で開始）
# 理由: FastAPI/Uvicorn起動時に既にイベントループが動作しているため、
#      MCPクライアント初期化時のasyncio.run()がRuntimeErrorを引き起こす。
#      遅延初期化により、最初のリクエスト処理時（リクエストハンドラ内）で
#      初期化することで、このイベントループ競合問題を回避する。
agent = None


async def get_agent():
    """
    エージェントを遅延初期化で取得（非同期版）

    最初の呼び出し時のみcreate_agent()を実行し、以降は同じインスタンスを再利用。
    これにより：
    - FastAPIのイベントループ問題を回避
    - MCPクライアント初期化は1回だけ実行（パフォーマンス維持）
    - 2回目以降のリクエストは高速処理
    """
    global agent
    if agent is None:
        # 最初のリクエスト時のみ実行される（Singleton Pattern）
        agent = await create_agent()
    return agent


# リクエストBody用のモデル
class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    start_time = time.time()
    logger.info(f"クエリ処理開始: {request.query}")

    try:
        # エージェントを遅延取得（初回のみ初期化処理が実行される）
        agent_start = time.time()
        current_agent = await get_agent()
        agent_time = time.time() - agent_start
        logger.info(f"エージェント取得完了: {agent_time:.2f}秒")

        # ユーザーのクエリをHumanMessageに変換
        messages = [HumanMessage(content=request.query)]

        # エージェントで回答を生成（非同期処理でMCPサーバーからの応答を適切に待つ）
        generation_start = time.time()
        ai_message = await run_agent(current_agent, messages)
        generation_time = time.time() - generation_start

        total_time = time.time() - start_time
        logger.info(
            f"クエリ処理完了: 生成時間={generation_time:.2f}秒, 総時間={total_time:.2f}秒"
        )

        return {"query": request.query, "answer": ai_message.content}
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(
            f"クエリ処理中にエラーが発生しました (処理時間: {error_time:.2f}秒): {e}"
        )
        raise HTTPException(
            status_code=500, detail=f"内部エラーが発生しました: {str(e)}"
        )


# サーバー起動設定（大型モデル対応）
if __name__ == "__main__":
    import uvicorn

    # gpt-oss:20bなど大型モデルの処理時間（63.97秒）に対応したタイムアウト設定
    logger.info("AIエージェントサーバーを起動します (大型モデル対応タイムアウト設定)")
    logger.info("Keep-alive timeout: 300秒, 大型モデル処理に対応")

    # シンプルなuvicorn起動（Config設定でのエラーを回避）
    uvicorn.run(
        app,  # app オブジェクトを直接指定
        host="0.0.0.0",
        port=8000,
        reload=False,  # reload=Falseで安定化
        # HTTP接続レベルのタイムアウト設定
        timeout_keep_alive=300,  # Keep-alive タイムアウトを5分に設定
        timeout_graceful_shutdown=30,  # グレースフルシャットダウンタイムアウト
        loop="asyncio",
        log_level="info",
    )
