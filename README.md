# RAG AI Agent with Dual MCP

MCP サーバーとの標準入出力(STDIO)方式と HTTP 方式の両方を同時使用する AI エージェントシステム

## 機能

- **デュアル MCP 接続**: STDIO + HTTP 両方の通信方式を同時使用
- **自律的ツール選択**: エージェントが最適な MCP ツールを自動選択
- **Web 検索統合**: Tavily 検索との連携
- **FastAPI 提供**: REST エンドポイントでの利用

## 環境要件

- Python 3.12 以上
- uv

## セットアップ

### 1. Git 設定

リポジトリをクローンした後、以下のコマンドを実行してください：

```bash
git config --global core.autocrlf false
```

※上記は、チェックアウト時、コミット時に改行コードを変更しない設定です（.gitattributes のままになります）

### 2. 仮想環境（.venv）の作成

仮想環境（`.venv`ディレクトリ）は GitHub リポジトリに登録されていないため、pull した後に仮想環境を作成する必要がある。

```コマンド（Windows Power Shell）
uv venv --python 3.12
```

※ `uv init`コマンドの実行は不要（pyproject.toml の作成などは作成済みのものが GitHub にプッシュされている）

### 3. .python-version の更新

```コマンド（Windows Power Shell）
uv python pin 3.12
```

※ `.python-version`が更新される。GitHub に登録されていない場合は新規作成される。

### 4. 依存関係のインストール

pyproject.toml に定義された依存関係をインストール：

```bash
uv sync
```

## 📋 使用例

### FastAPI 経由での利用

```bash
# サーバー起動
uvicorn agent_api:app --reload --port 8000

# ブラウザでSwagger UI
http://127.0.0.1:8000/docs
```

### プログラムからの利用

```python
from agent_core import create_agent, run_agent
from langchain_core.messages import HumanMessage

# エージェント作成（STDIO + HTTP両方のMCPツールを含む）
agent = create_agent()

# クエリ実行
messages = [HumanMessage(content="セキュリティポリシーについて教えて")]
response = run_agent(agent, messages)
print(response.content)
```

## � MCP クライアント

このシステムは、2 つの異なる通信方式で MCP サーバーと連携します：

### STDIO 方式

- **ファイル**: `mcp_client_fastmcp/stdio_client.py`
- **特徴**: プロセス間通信による直接的な接続、高速
- **用途**: ローカルファイル（docx, pdf）への直接アクセス

### HTTP 方式

- **ファイル**: `mcp_client_fastmcp/http_client.py`
- **特徴**: HTTP API 経由のリモートアクセス、スケーラブル
- **用途**: 分散環境での MCP サーバー接続

詳細な実装情報については、[HTTP MCP クライアント技術仕様](docs/HTTP_MCP_CLIENT_README.md)を参照してください。

## �🛠️ 設定

### デフォルト設定

- **STDIO サーバー**: `D:\vscode_projects\sample_rag_mcp_server_stdio\rag_mcp_server_stdio.py`
- **HTTP サーバー**: `http://127.0.0.1:8001/mcp`
- **モデル**: `llama3.1:8b`

### 設定変更

各クライアントモジュール内の定数を変更してください：

- `mcp_client_fastmcp/stdio_client.py`: STDIO 設定
- `mcp_client_fastmcp/http_client.py`: HTTP 設定

## 📚 ドキュメント

- [HTTP MCP クライアント技術仕様](docs/HTTP_MCP_CLIENT_README.md) - HTTP 方式の詳細実装
- [動的ツール情報取得の実装](docs/DYNAMIC_TOOL_INFO_COMPLETE.md) - MCP サーバーからの動的情報取得
