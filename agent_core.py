# agent_core.py
from dotenv import load_dotenv
from typing import List
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.tools import Tool

# from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from mcp_client_langchain_adapters.mcp_tools_factory import create_mcp_tools
from config import LLM_MODEL, OLLAMA_MODEL_PREFIX
from logger import get_logger

# ロガー設定
logger = get_logger(__name__)


async def create_agent(model_name: str = LLM_MODEL):
    """
    指定したモデルによりエージェントを構築

    Args:
        model_name: 使用するLLMモデル名
    """
    try:
        # APIキー読み込み
        load_dotenv(override=True)

        # モデル初期化（ollama_sample.pyと同じアプローチ）
        if model_name.startswith(OLLAMA_MODEL_PREFIX):
            # Ollamaのローカルモデルの場合はChatOllamaを使用
            model = ChatOllama(model=model_name, temperature=0.5)
            logger.info(f"Ollamaモデルを初期化しました: {model_name}")
        else:
            # その他のモデル（Anthropic, OpenAI, Google等）
            model = init_chat_model(model_name)
            logger.info(f"外部モデルを初期化しました: {model_name}")

        # # Web検索ツール（ツール利用のサンプルとして実装）
        # web_search_tool = TavilySearch(max_results=5)

        # MCPクライアントツール準備（langchain-mcp-adapters使用）
        logger.info(">>> langchain-mcp-adapters を使用してMCPツールを作成")
        mcp_tools: List[Tool] = await create_mcp_tools()

        # # 利用するツール一覧
        # tools = [web_search_tool] + mcp_tools
        # 利用するツール一覧
        tools = []
        tools.extend(mcp_tools)

        # プロンプトを動的に生成（MCPツールの実際の名前と説明を使用）
        base_prompt = (
            "社内資料に基づき、業務の質問に根拠付きで回答してください。"
            "必要に応じてネットも検索してください。"
        )

        # MCPツールの情報を動的に追加
        mcp_tools_info = []
        for tool in tools:
            # web_search_tool以外のMCPツールを対象にする
            if hasattr(tool, "func") and hasattr(tool.func, "_mcp_meta"):
                transport = tool.func._mcp_meta.get("transport", "unknown")
                transport_label = {
                    "stdio": "標準入出力方式",
                    "http": "Streamable HTTP方式",
                }.get(transport, transport)
                mcp_tools_info.append(
                    f"- {tool.name}: {tool.description} ({transport_label})"
                )

        if mcp_tools_info:
            prompt = (
                base_prompt
                + "\n複数のMCPツールが利用可能な場合は、それぞれの特徴に応じて適切なツールを選択してください。\n"
                + "\n".join(mcp_tools_info)
            )
        else:
            prompt = base_prompt

        # エージェント作成
        agent = create_react_agent(
            model=model,
            tools=tools,
            prompt=prompt,
        )

        logger.info(f">>> エージェント作成完了。利用可能ツール数: {len(tools)}")
        return agent

    except Exception as e:
        logger.error(f"エージェント作成中にエラーが発生しました: {e}")
        raise


async def create_default_agent():
    """
    標準設定でエージェントを作成
    langchain-mcp-adapters を使用してSTDIOとStreamable HTTP両方のMCPクライアントを同時使用
    """
    return await create_agent(LLM_MODEL)


async def run_agent(agent, messages: List[BaseMessage]) -> AIMessage:
    """
    エージェントにメッセージを投げて最終的な応答だけ返す（非同期版）

    Args:
        agent: LangGraphエージェントインスタンス
        messages: 送信するメッセージのリスト

    Returns:
        AIMessage: エージェントからの最終応答メッセージ

    使い方:
        # FastAPI や CLI など「確定応答だけ欲しい」場合に利用する
        ai_message = await run_agent(agent, messages)
        logger.info(ai_message.content)
    """
    try:
        last = None
        # astream を使用して非同期ストリーム処理
        async for s in agent.astream({"messages": messages}, stream_mode="values"):
            last = s["messages"]
        return last[-1]  # AIMessage
    except Exception as e:
        logger.error(f"エージェント実行中にエラーが発生しました: {e}")
        raise
