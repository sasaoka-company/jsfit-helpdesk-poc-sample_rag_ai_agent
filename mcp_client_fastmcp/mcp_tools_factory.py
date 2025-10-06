# mcp_client/factory.py
"""
MCPクライアント作成ファクトリー関数群
複数の通信方式（標準入出力、HTTP等）をサポートし、統一インターフェースを提供
"""

from typing import List
from langchain_core.tools import Tool

from .stdio_client import create_stdio_mcp_tools
from .http_client import create_http_mcp_tools
from logger import get_logger

logger = get_logger(__name__)


def create_mcp_tools() -> List[Tool]:
    """
    STDIO方式とStreamable HTTP方式の両方のMCPツールを作成する

    Returns:
        List[Tool]: STDIO方式とStreamable HTTP方式のMCPツールのリスト

    """
    logger.info(">>> MCPツール作成開始（STDIO・Streamable HTTP両方式）")

    # MCPツールリスト
    mcp_tools: List[Tool] = []

    # STDIO ツール作成
    try:
        stdio_tools: List[Tool] = create_stdio_mcp_tools()
        mcp_tools.extend(stdio_tools)
        stdio_tool_names = [t.name for t in stdio_tools]
        logger.info(f">>> MCPツール（STDIO）作成成功: {stdio_tool_names}")
    except Exception as e:
        logger.error(f">>> MCPツール（STDIO）作成失敗: {e}")
        raise

    # HTTP ツール作成
    try:
        http_tools: List[Tool] = create_http_mcp_tools()
        mcp_tools.extend(http_tools)
        http_tool_names = [t.name for t in http_tools]
        logger.info(f">>> MCPツール（Streamable HTTP）作成成功: {http_tool_names}")
    except Exception as e:
        logger.error(f">>> MCPツール（Streamable HTTP）作成失敗: {e}")
        raise

    # ツール名の重複チェック
    tool_names = [t.name for t in mcp_tools]
    duplicate_names = [name for name in tool_names if tool_names.count(name) > 1]

    if duplicate_names:
        error_msg = f"重複するMCPツール名が検出されました: {duplicate_names}"
        logger.error(f">>> {error_msg}")
        raise ValueError(error_msg)

    logger.info(f">>> 作成されたMCPツール数: {len(mcp_tools)}")
    tool_names = [t.name for t in mcp_tools]
    logger.info(f">>> 作成されたMCPツール名: {tool_names}")
    return mcp_tools
