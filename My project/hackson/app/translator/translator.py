"""
翻译管理器 - 协调整个翻译流程
"""
import re
import asyncio
from pathlib import Path
from typing import Callable, Optional, List, Dict

from app.parsers.base import ParsedDocument, ContentBlock, BlockType
from app.services.base import BaseAIService
from app.translator.pdf_generator import PDFGenerator


class TranslationManager:
    """翻译管理器"""
    
    # 最大块大小（字符数）
    MAX_CHUNK_SIZE = 3000
    
    def __init__(self, ai_service: BaseAIService):
        self.ai_service = ai_service
        self.pdf_generator = PDFGenerator()
    
    async def translate_to_pdf(
        self,
        document: ParsedDocument,
        output_path: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> Path:
        """
        翻译文档并生成 PDF
        保留原始图片和公式
        
        Args:
            document: 解析后的文档
            output_path: 输出 PDF 路径
            progress_callback: 进度回调
            
        Returns:
            输出文件路径
        """
        source_path = getattr(document, 'source_path', None)
        if not source_path:
            raise ValueError("文档缺少源文件路径")
            
        # 检查是否有详细的页面内容（用于精确布局还原）
        if hasattr(document, 'pages_content') and document.pages_content:
            return await self._translate_pdf_with_layout(document, output_path, progress_callback)
        
        # 降级方案：如果没有页面信息（比如不是PDF源或者是简单的解析器），无法做布局还原
        # 这里为了演示，抛出异常或仅做简单文本拼接（暂不支持）
        raise NotImplementedError("该文档类型不支持布局还原翻译")

    async def _translate_pdf_with_layout(
        self,
        document: ParsedDocument,
        output_path: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> Path:
        """使用页面布局信息进行精确翻译"""
        converted_pages = [] # List[Dict[block_idx, text]]
        
        total_pages = len(document.pages_content)
        
        for page_idx, page_content in enumerate(document.pages_content):
            if progress_callback:
                progress = int((page_idx / total_pages) * 90)
                progress_callback(progress, f"正在翻译第 {page_idx + 1}/{total_pages} 页...")
            
            page_translations = {}
            
            # 收集该页所有的文本块
            blocks_to_translate = []
            block_indices = []
            
            for b_idx, block in enumerate(page_content.text_blocks):
                text = block.get("text", "").strip()
                if not text:
                    continue
                # 简单过滤掉纯数字或太短的非句文本（可选）
                if len(text) < 2 and text.isdigit():
                    continue
                
                # 过滤掉数学公式块 (不翻译，pdf生成时会自动跳过)
                is_formula = False
                # 常见的整段公式模式
                formula_patterns = [
                    r'^\s*\$\$[\s\S]*?\$\$\s*$',
                    r'^\s*\\begin\{equation\}[\s\S]*?\\end\{equation\}\s*$',
                    r'^\s*\\begin\{align\}[\s\S]*?\\end\{align\}\s*$',
                    r'^\s*\\\[[\s\S]*?\\\]\s*$'
                ]
                import re # Ensure re is available inside function if not global, but usually global
                
                for pattern in formula_patterns:
                    if re.match(pattern, text, re.IGNORECASE):
                        is_formula = True
                        break
                
                if is_formula:
                    continue

                blocks_to_translate.append(text)
                block_indices.append(b_idx)
            
            if not blocks_to_translate:
                converted_pages.append({})
                continue
                
            # 批量翻译（为了提高速度，可以将一页的文本合并发送）
            # 这里简单实现：逐块或合并翻译
            # 为了保持块的独立性以便回填，我们将它们组合成一个列表提示给 AI，或者分别翻译
            # 考虑到上下文，最好是整页文本一起给 AI，请求返回对应的翻译列表
            # 但为了鲁棒性，这里先逐块翻译（或者小批量）
            
            # 简易策略：逐块调用 (注意：这会很慢，但在 Hackathon 项目中可接受)
            # 优化策略：合并为一个大文本，用特殊分隔符，然后分割
            
            combined_text = "\n---BLOCK_SEP---\n".join(blocks_to_translate)
            
            try:
                # 提示 AI 保持分隔符
                system_prompt = "You are a translator. Translate the following text segments into Chinese. Maintain the number of segments. Segments are separated by '---BLOCK_SEP---'. Return ONLY the translated segments separated by '---BLOCK_SEP---'."
                # 注意：BaseAIService 可能没有 system_prompt 参数，视具体实现而定
                # 这里假设 direct translate
                
                # 由于我们无法修改 ai_service 接口，这里只能调用 translate
                # 我们假设 translate 只是简单的 text -> translated text
                # 尝试分块翻译
                
                # 并发翻译该页所有块
                tasks = [self.ai_service.translate(text) for text in blocks_to_translate]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for i, res in enumerate(results):
                    original_idx = block_indices[i]
                    if isinstance(res, Exception):
                        # 翻译失败，使用原文
                        page_translations[original_idx] = blocks_to_translate[i]
                    else:
                        page_translations[original_idx] = res.strip()
                        
            except Exception as e:
                print(f"Page {page_idx} translation error: {e}")
            
            converted_pages.append(page_translations)
            
        if progress_callback:
            progress_callback(95, "正在生成最终 PDF...")
            
        # 生成 PDF
        return self.pdf_generator.generate_layout_preserved(
            source_pdf_path=document.source_path,
            translated_pages=converted_pages,
            output_path=output_path
        )

    
    async def translate_document(
        self,
        document: ParsedDocument,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> str:
        """
        翻译整个文档
        
        Args:
            document: 解析后的文档
            progress_callback: 进度回调函数 (progress: 0-100, message: str)
            
        Returns:
            翻译后的 Markdown 文本
        """
        translatable_blocks = document.get_translatable_blocks()
        total_blocks = len(translatable_blocks)
        
        if total_blocks == 0:
            return document.raw_content
        
        # 分块处理
        chunks = self._create_chunks(translatable_blocks)
        total_chunks = len(chunks)
        
        if progress_callback:
            progress_callback(0, f"共 {total_chunks} 个翻译块，开始翻译...")
        
        # 翻译所有块
        translated_blocks = {}
        
        for i, (block_indices, chunk_text) in enumerate(chunks):
            if progress_callback:
                progress = int((i / total_chunks) * 100)
                progress_callback(progress, f"正在翻译第 {i + 1}/{total_chunks} 块...")
            
            try:
                translated_text = await self.ai_service.translate(chunk_text)
                
                # 如果是单个块，直接映射
                if len(block_indices) == 1:
                    translated_blocks[block_indices[0]] = translated_text
                else:
                    # 多个块合并翻译，需要分割回去
                    self._split_translated_text(
                        block_indices, 
                        chunk_text, 
                        translated_text, 
                        translatable_blocks,
                        translated_blocks
                    )
            except Exception as e:
                # 翻译失败，保留原文
                for idx in block_indices:
                    translated_blocks[idx] = f"[翻译失败: {str(e)}]\n{translatable_blocks[idx].content}"
        
        if progress_callback:
            progress_callback(100, "翻译完成，正在组装文档...")
        
        # 组装最终文档
        return self._assemble_document(document, translatable_blocks, translated_blocks)
    
    def _create_chunks(
        self, 
        blocks: List[ContentBlock]
    ) -> List[tuple]:
        """
        将块分组为适合 AI 处理的大小
        
        Returns:
            List of (block_indices, combined_text)
        """
        chunks = []
        current_indices = []
        current_text = ""
        
        for i, block in enumerate(blocks):
            block_text = self._prepare_block_for_translation(block)
            
            # 如果单个块就超过限制，单独处理
            if len(block_text) > self.MAX_CHUNK_SIZE:
                # 先保存当前累积的块
                if current_indices:
                    chunks.append((current_indices, current_text))
                    current_indices = []
                    current_text = ""
                
                # 单独添加这个大块
                chunks.append(([i], block_text))
                continue
            
            # 检查是否可以添加到当前块
            if len(current_text) + len(block_text) + 2 <= self.MAX_CHUNK_SIZE:
                current_indices.append(i)
                if current_text:
                    current_text += "\n\n"
                current_text += block_text
            else:
                # 保存当前块，开始新块
                if current_indices:
                    chunks.append((current_indices, current_text))
                current_indices = [i]
                current_text = block_text
        
        # 保存最后一个块
        if current_indices:
            chunks.append((current_indices, current_text))
        
        return chunks
    
    def _prepare_block_for_translation(self, block: ContentBlock) -> str:
        """准备块文本用于翻译"""
        text = block.content
        
        # 如果包含公式，添加特殊标记
        if block.metadata.get("has_formula"):
            # 保护 LaTeX 公式
            text = self._protect_formulas(text)
        
        return text
    
    def _protect_formulas(self, text: str) -> str:
        """保护数学公式不被翻译"""
        # 标记公式（翻译后需要恢复）
        # 这里简单返回原文，依靠 AI 的系统提示词来保护公式
        return text
    
    def _split_translated_text(
        self,
        block_indices: List[int],
        original_text: str,
        translated_text: str,
        original_blocks: List[ContentBlock],
        translated_blocks: dict
    ):
        """将合并翻译的文本分割回各个块"""
        # 简单策略：按段落分割
        translated_paragraphs = translated_text.split('\n\n')
        
        if len(translated_paragraphs) >= len(block_indices):
            # 足够的段落，按顺序分配
            for i, idx in enumerate(block_indices):
                if i < len(translated_paragraphs):
                    translated_blocks[idx] = translated_paragraphs[i]
                else:
                    translated_blocks[idx] = ""
        else:
            # 段落不够，将所有内容分配给第一个块，其余为空
            translated_blocks[block_indices[0]] = translated_text
            for idx in block_indices[1:]:
                translated_blocks[idx] = ""
    
    def _assemble_document(
        self,
        document: ParsedDocument,
        translatable_blocks: List[ContentBlock],
        translated_blocks: dict
    ) -> str:
        """组装翻译后的文档"""
        result_parts = []
        
        # 添加元数据
        if document.metadata.title:
            result_parts.append(f"# {document.metadata.title}\n")
        
        # 创建块索引映射
        translatable_indices = {
            id(block): i for i, block in enumerate(translatable_blocks)
        }
        
        # 按原始顺序组装
        for block in document.blocks:
            if block.should_translate:
                # 查找翻译后的内容
                idx = translatable_indices.get(id(block))
                if idx is not None and idx in translated_blocks:
                    content = translated_blocks[idx]
                else:
                    content = block.content
                
                # 根据块类型格式化
                if block.type == BlockType.HEADING:
                    # 保持 Markdown 标题格式
                    if not content.startswith('#'):
                        prefix = '#' * block.level + ' '
                        content = prefix + content
                    result_parts.append(content)
                else:
                    result_parts.append(content)
            else:
                # 不需要翻译的块保持原样
                result_parts.append(block.content)
        
        return '\n\n'.join(result_parts)
