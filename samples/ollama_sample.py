# ollama_core.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# .envファイルから環境変数を読み込み
load_dotenv()

# LLMモデル
# Ollamaのモデル名（llama3:8b-elyza-jp）を指定
llm = ChatOpenAI(model="llama3:8b-elyza-jp", temperature=0)


# 質問に対してLLMが直接回答する関数
def query(text: str):
    # RAG関連のコードは削除
    # LLMが直接、ユーザーの入力に答える
    answer = llm.invoke(text)
    return answer.content
