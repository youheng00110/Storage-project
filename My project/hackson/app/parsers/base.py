"""
文件解析器基类
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
from enum import Enum


class BlockType(Enum):
    """内容块类型"""
    TEXT = "text"           # 普通文本（需要翻译）
    HEADING = "heading"     # 标题（需要翻译）
    FORMULA = "formula"     # 数学公式（不翻译）
    CODE = "code"           # 代码块（不翻译）
    REFERENCE = "reference" # 引用（不翻译）
    TABLE = "table"         # 表格（部分翻译）
    FIGURE = "figure"       # 图表标题（需要翻译）
    METADATA = "metadata"   # 元数据（不翻译）


@dataclass
class ContentBlock:
    """文档内容块"""
    type: BlockType
    content: str
    should_translate: bool = True
    level: int = 0  # 用于标题层级
    metadata: dict = field(default_factory=dict)


@dataclass
class DocumentMetadata:
    """文档元数据"""
    title: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    keywords: List[str] = field(default_factory=list)


@dataclass
class ParsedDocument:
    """解析后的文档结构"""
    metadata: DocumentMetadata
    blocks: List[ContentBlock]
    raw_content: str = ""
    
    def get_translatable_blocks(self) -> List[ContentBlock]:
        """获取需要翻译的块"""
        return [b for b in self.blocks if b.should_translate]


class BaseParser(ABC):
    """文件解析器基类"""
    
    @abstractmethod
    def parse(self, file_path: Path) -> ParsedDocument:
        """
        解析文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            ParsedDocument: 解析后的文档结构
        """
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """获取支持的文件扩展名"""
        pass
