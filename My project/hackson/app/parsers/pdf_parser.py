"""
PDF 文件解析器 - 使用 PyMuPDF 提取文本和图片
"""
import re
import io
import base64
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field

import fitz  # PyMuPDF

from .base import (
    BaseParser, ParsedDocument, ContentBlock, 
    DocumentMetadata, BlockType
)


@dataclass
class ImageInfo:
    """图片信息"""
    data: bytes
    ext: str
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1)
    page_num: int
    width: float
    height: float


@dataclass
class PageContent:
    """页面内容"""
    page_num: int
    width: float
    height: float
    text_blocks: List[Dict[str, Any]] = field(default_factory=list)
    images: List[ImageInfo] = field(default_factory=list)


class PDFParser(BaseParser):
    """PDF 文件解析器 - 保留图片和布局"""
    
    # LaTeX 公式模式
    LATEX_PATTERNS = [
        r'\$\$[\s\S]*?\$\$',
        r'\$[^\$\n]+?\$',
        r'\\begin\{equation\}[\s\S]*?\\end\{equation\}',
        r'\\begin\{align\}[\s\S]*?\\end\{align\}',
    ]
    
    def __init__(self):
        self.pages_content: List[PageContent] = []
        self.images: List[ImageInfo] = []
    
    def parse(self, file_path: Path) -> ParsedDocument:
        """解析 PDF 文件，提取文本和图片"""
        doc = fitz.open(str(file_path))
        
        self.pages_content = []
        self.images = []
        full_text = ""
        
        for page_num, page in enumerate(doc):
            page_content = PageContent(
                page_num=page_num,
                width=page.rect.width,
                height=page.rect.height
            )
            
            # 提取文本块（带位置信息）
            text_dict = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:  # 文本块
                    block_text = ""
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            block_text += span.get("text", "")
                        block_text += "\n"
                    
                    if block_text.strip():
                        page_content.text_blocks.append({
                            "text": block_text.strip(),
                            "bbox": block.get("bbox"),
                            "lines": block.get("lines", [])
                        })
                        full_text += block_text + "\n"
            
            # 提取图片
            for img_index, img in enumerate(page.get_images(full=True)):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # 获取图片在页面上的位置
                    img_rects = page.get_image_rects(xref)
                    if img_rects:
                        rect = img_rects[0]
                        image_info = ImageInfo(
                            data=image_bytes,
                            ext=image_ext,
                            bbox=(rect.x0, rect.y0, rect.x1, rect.y1),
                            page_num=page_num,
                            width=rect.width,
                            height=rect.height
                        )
                        page_content.images.append(image_info)
                        self.images.append(image_info)
                except Exception as e:
                    print(f"提取图片失败: {e}")
            
            self.pages_content.append(page_content)
            full_text += "\n\n"
        
        doc.close()
        
        # 解析文档结构
        metadata = self._extract_metadata(full_text)
        blocks = self._parse_content(full_text)
        
        # 在 ParsedDocument 中存储额外信息
        parsed_doc = ParsedDocument(
            metadata=metadata,
            blocks=blocks,
            raw_content=full_text
        )
        
        # 添加额外属性
        parsed_doc.pages_content = self.pages_content
        parsed_doc.images = self.images
        parsed_doc.source_path = file_path
        
        return parsed_doc
    
    def _extract_metadata(self, text: str) -> DocumentMetadata:
        """提取文档元数据"""
        metadata = DocumentMetadata()
        
        # 尝试从文本中提取摘要
        abstract_match = re.search(
            r'(?:Abstract|ABSTRACT)[:\s]*\n?([\s\S]*?)(?=\n\s*(?:Keywords|KEYWORDS|Introduction|INTRODUCTION|1\.|1\s))',
            text,
            re.IGNORECASE
        )
        if abstract_match:
            metadata.abstract = abstract_match.group(1).strip()
        
        return metadata
    
    def _parse_content(self, text: str) -> List[ContentBlock]:
        """解析文档内容为块"""
        blocks = []
        paragraphs = re.split(r'\n\s*\n', text)
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # 检查是否是标题
            if self._is_heading(para):
                level = self._get_heading_level(para)
                blocks.append(ContentBlock(
                    type=BlockType.HEADING,
                    content=para,
                    should_translate=True,
                    level=level
                ))
            # 检查是否是参考文献
            elif self._is_reference(para):
                blocks.append(ContentBlock(
                    type=BlockType.REFERENCE,
                    content=para,
                    should_translate=False
                ))
            # 检查是否包含公式
            elif self._contains_formula(para):
                blocks.append(ContentBlock(
                    type=BlockType.TEXT,
                    content=para,
                    should_translate=True,
                    metadata={"has_formula": True}
                ))
            # 检查是否是图表标题
            elif self._is_figure_caption(para):
                blocks.append(ContentBlock(
                    type=BlockType.FIGURE,
                    content=para,
                    should_translate=True,
                    metadata={"is_caption": True}
                ))
            else:
                blocks.append(ContentBlock(
                    type=BlockType.TEXT,
                    content=para,
                    should_translate=True
                ))
        
        return blocks
    
    def _is_heading(self, text: str) -> bool:
        """判断是否是标题"""
        if re.match(r'^(\d+\.)+\s*\w', text):
            return True
        if re.match(
            r'^(Abstract|Introduction|Conclusion|References|'
            r'Background|Methods?|Results?|Discussion|'
            r'Acknowledgements?|Appendix)',
            text,
            re.IGNORECASE
        ):
            return True
        if len(text) < 100 and text and text[0].isupper() and '\n' not in text:
            words = text.split()
            if len(words) <= 10:
                return True
        return False
    
    def _get_heading_level(self, text: str) -> int:
        """获取标题层级"""
        match = re.match(r'^((\d+\.)+)', text)
        if match:
            return len(match.group(1).split('.')) - 1
        return 1
    
    def _is_reference(self, text: str) -> bool:
        """判断是否是参考文献"""
        if re.match(r'^\[?\d+[\]\.)]', text):
            return True
        return False
    
    def _is_figure_caption(self, text: str) -> bool:
        """判断是否是图表标题"""
        if re.match(r'^(Figure|Fig\.|Table|Tab\.)\s*\d+', text, re.IGNORECASE):
            return True
        return False
    
    def _contains_formula(self, text: str) -> bool:
        """检查是否包含数学公式"""
        for pattern in self.LATEX_PATTERNS:
            if re.search(pattern, text):
                return True
        return False
    
    def get_supported_extensions(self) -> List[str]:
        return [".pdf"]
