"""
文件解析器工厂
"""
from pathlib import Path

from .base import BaseParser
from .pdf_parser import PDFParser
from .docx_parser import DocxParser
from .markdown_parser import MarkdownParser


def create_parser(file_extension: str) -> BaseParser:
    """
    根据文件扩展名创建解析器
    
    Args:
        file_extension: 文件扩展名（如 .pdf, .docx, .md）
        
    Returns:
        BaseParser: 对应的解析器实例
    """
    ext = file_extension.lower()
    
    parsers = {
        ".pdf": PDFParser,
        ".docx": DocxParser,
        ".md": MarkdownParser,
        ".markdown": MarkdownParser,
        ".txt": MarkdownParser,  # 纯文本用 Markdown 解析器处理
    }
    
    if ext not in parsers:
        raise ValueError(
            f"不支持的文件类型: {ext}。"
            f"支持的类型: {', '.join(parsers.keys())}"
        )
    
    return parsers[ext]()


def get_supported_extensions() -> list:
    """获取所有支持的文件扩展名"""
    return [".pdf", ".docx", ".md", ".markdown", ".txt"]
