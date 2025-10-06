# config.py
"""
プロジェクト全体の定数を管理するモジュール
"""

# ========================================
# MCPサーバー設定（HTTP方式用）
# ========================================
HTTP_SERVER_URL = "http://127.0.0.1:8001/mcp"  # デフォルトのHTTPサーバーURL
HTTP_TIMEOUT = 30  # タイムアウト設定（秒）

# ========================================
# MCPサーバー設定（標準入出力方式用）
# ========================================
STDIO_PYTHON_EXECUTABLE = "D:\\github_projects\\jsfit-helpdesk-poc-sample_rag_mcp_server_stdio\\.venv\\Scripts\\python.exe"
STDIO_SERVER_SCRIPT = "D:\\github_projects\\jsfit-helpdesk-poc-sample_rag_mcp_server_stdio\\rag_mcp_server_stdio.py"

# ========================================
# 使用するLLMモデル
# ========================================
LLM_MODEL = "llama3.1:8b"
# LLM_MODEL = "gpt-oss:20b"  # 20Bパラメータモデル - 処理時間が長いため注意
# LLM_MODEL = "openai:gpt-5-nano"
# LLM_MODEL = "google_genai:gemini-2.5-flash-lite"
# LLM_MODEL = "anthropic:claude-3-haiku-20240307"

# ローカルモデル（Ollama）の識別子
# Ollamaライブラリに含まれるモデルのプレフィックス
OLLAMA_MODEL_PREFIX = ("llama3.1", "gpt-oss", "mistral")  # 必要に応じて追加
