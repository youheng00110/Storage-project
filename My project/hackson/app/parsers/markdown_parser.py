"""
Markdown 文件解析器
"""
import re
from pathlib import Path
from typing import List

from .base import (
    BaseParser, ParsedDocument, ContentBlock, 
    DocumentMetadata, BlockType
)


class MarkdownParser(BaseParser):
    """Markdown 文件解析器"""
    
    # 代码块模式
    CODE_BLOCK_PATTERN = r'```[\s\S]*?```'
    
    # LaTeX 公式模式
    LATEX_PATTERNS = [
        r'\$\$[\s\S]*?\$\$',
        r'\$[^\$\n]+?\$',
    ]
    
    def parse(self, file_path: Path) -> ParsedDocument:
        """解析 Markdown 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = self._extract_metadata(content)
        blocks = self._parse_content(content)
        
        return ParsedDocument(
            metadata=metadata,
            blocks=blocks,
            raw_content=content
        )
    
    def _extract_metadata(self, content: str) -> DocumentMetadata:
        """提取文档元数据（YAML front matter）"""
        metadata = DocumentMetadata()
        
        # 检查 YAML front matter
        yaml_match = re.match(r'^---\s*\n([\s\S]*?)\n---', content)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            
            # 简单解析 YAML
            title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', yaml_content, re.MULTILINE)
            if title_match:
                metadata.title = title_match.group(1)
            
            author_match = re.search(r'author:\s*["\']?(.+?)["\']?\s*$', yaml_content, re.MULTILINE)
            if author_match:
                metadata.authors = [author_match.group(1)]
        
        # 如果没有 front matter，尝试从第一个 H1 标题获取
        if not metadata.title:
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                metadata.title = h1_match.group(1)
        
        return metadata
    
    def _parse_content(self, content: str) -> List[ContentBlock]:
        """解析 Markdown 内容"""
        blocks = []
        
        # 移除 YAML front matter
        content = re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n?', '', content)
        
        # 先提取代码块，用占位符替换
        code_blocks = []
        def save_code_block(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks) - 1}__"
        
        content = re.sub(self.CODE_BLOCK_PATTERN, save_code_block, content)
        
        # 按行处理
        lines = content.split('\n')
        current_paragraph = []
        
        for line in lines:
            stripped = line.strip()
            
            # 空行表示段落结束
            if not stripped:
                if current_paragraph:
                    blocks.extend(self._process_paragraph('\n'.join(current_paragraph)))
                    current_paragraph = []
                continue
            
            # 检查是否是代码块占位符
            code_match = re.match(r'__CODE_BLOCK_(\d+)__', stripped)
            if code_match:
                if current_paragraph:
                    blocks.extend(self._process_paragraph('\n'.join(current_paragraph)))
                    current_paragraph = []
                
                idx = int(code_match.group(1))
                blocks.append(ContentBlock(
                    type=BlockType.CODE,
                    content=code_blocks[idx],
                    should_translate=False
                ))
                continue
            
            # 检查是否是标题
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            if heading_match:
                if current_paragraph:
                    blocks.extend(self._process_paragraph('\n'.join(current_paragraph)))
                    current_paragraph = []
                
                level = len(heading_match.group(1))
                blocks.append(ContentBlock(
                    type=BlockType.HEADING,
                    content=stripped,
                    should_translate=True,
                    level=level
                ))
                continue
            
            # 普通行，添加到当前段落
            current_paragraph.append(line)
        
        # 处理最后一个段落
        if current_paragraph:
            blocks.extend(self._process_paragraph('\n'.join(current_paragraph)))
        
        return blocks
    
    def _process_paragraph(self, text: str) -> List[ContentBlock]:
        """处理段落文本"""
        blocks = []
        text = text.strip()
        
        if not text:
            return blocks
        
        # 检查是否是引用块
        if text.startswith('>'):
            blocks.append(ContentBlock(
                type=BlockType.TEXT,
                content=text,
                should_translate=True,
                metadata={"is_quote": True}
            ))
            return blocks
        
        # 检查是否是参考文献格式
        if re.match(r'^\[?\d+[\]\.)]', text):
            blocks.append(ContentBlock(
                type=BlockType.REFERENCE,
                content=text,
                should_translate=False
            ))
            return blocks
        
        # 检查是否包含公式
        has_formula = any(re.search(p, text) for p in self.LATEX_PATTERNS)
        
        blocks.append(ContentBlock(
            type=BlockType.TEXT,
            content=text,
            should_translate=True,
            metadata={"has_formula": has_formula} if has_formula else {}
        ))
        
        return blocks
    
    def get_supported_extensions(self) -> List[str]:
        return [".md", ".markdown", ".txt"]
