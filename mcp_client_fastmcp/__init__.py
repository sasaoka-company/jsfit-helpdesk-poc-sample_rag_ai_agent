# mcp_client/__init__.py
"""
MCPクライアント統合モジュール
STDIO方式とHTTP方式の両方でMCPサーバーと連携するツールを提供
"""

# メイン機能をインポートして公開
from .mcp_tools_factory import create_mcp_tools

# パッケージの公開API
__all__ = ["create_mcp_tools"]
