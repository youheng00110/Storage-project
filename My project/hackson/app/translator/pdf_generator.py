"""
PDF 生成器 - 生成保留图片和布局的翻译后 PDF
"""
import io
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class PDFGenerator:
    """PDF 生成器 - 保留原始布局和图片"""
    
    def __init__(self):
        self._register_fonts()
    
    def _register_fonts(self):
        """注册中文字体"""
        # 尝试注册系统中文字体
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",      # 黑体
            "C:/Windows/Fonts/simsun.ttc",       # 宋体
            "C:/Windows/Fonts/msyh.ttc",         # 微软雅黑
            "C:/Windows/Fonts/simkai.ttf",       # 楷体
        ]
        
        self.chinese_font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font_name = Path(font_path).stem
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    self.chinese_font = font_name
                    break
                except Exception:
                    continue
        
        if not self.chinese_font:
            self.chinese_font = "Helvetica"  # 后备字体
    
    def generate_from_original(
        self,
        source_pdf_path: Path,
        translated_texts: Dict[int, str],
        output_path: Path
    ) -> Path:
        """
        基于原始 PDF 生成翻译后的 PDF
        在原文下方添加译文，保留所有图片
        
        Args:
            source_pdf_path: 原始 PDF 路径
            translated_texts: 翻译后的文本 {block_index: translated_text}
            output_path: 输出路径
            
        Returns:
            输出文件路径
        """
        # 打开原始 PDF
        doc = fitz.open(str(source_pdf_path))
        
        # 创建新文档用于输出
        output_doc = fitz.open()
        
        block_index = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 创建新页面，尺寸增大以容纳译文
            new_width = page.rect.width
            new_height = page.rect.height * 1.8  # 增加高度以容纳译文
            
            new_page = output_doc.new_page(
                width=new_width,
                height=new_height
            )
            
            # 复制原始页面内容到新页面顶部
            new_page.show_pdf_page(
                fitz.Rect(0, 0, page.rect.width, page.rect.height),
                doc,
                page_num
            )
            
            # 在原文下方添加分隔线
            separator_y = page.rect.height + 10
            new_page.draw_line(
                fitz.Point(20, separator_y),
                fitz.Point(new_width - 20, separator_y),
                color=(0.7, 0.7, 0.7),
                width=1
            )
            
            # 添加"译文"标签
            new_page.insert_text(
                fitz.Point(20, separator_y + 20),
                "【译文】",
                fontsize=12,
                fontname="china-s",  # 使用内置中文字体
                color=(0.3, 0.3, 0.3)
            )
            
            # 提取原页面文本块
            text_dict = page.get_text("dict")
            y_offset = separator_y + 40
            
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:  # 文本块
                    # 获取原始文本
                    original_text = ""
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            original_text += span.get("text", "")
                        original_text += " "
                    
                    original_text = original_text.strip()
                    if not original_text:
                        continue
                    
                    # 获取翻译后的文本
                    translated_text = translated_texts.get(block_index, original_text)
                    
                    # 插入翻译文本
                    try:
                        text_rect = fitz.Rect(
                            20, y_offset,
                            new_width - 20, y_offset + 200
                        )
                        
                        # 使用内置中文字体
                        rc = new_page.insert_textbox(
                            text_rect,
                            translated_text,
                            fontsize=10,
                            fontname="china-s",
                            align=fitz.TEXT_ALIGN_LEFT
                        )
                        
                        # 计算实际使用的高度
                        if rc > 0:
                            y_offset += rc + 15
                        else:
                            y_offset += 50
                            
                    except Exception as e:
                        # 如果中文字体失败，尝试使用默认字体
                        try:
                            new_page.insert_text(
                                fitz.Point(20, y_offset),
                                translated_text[:100] + "..." if len(translated_text) > 100 else translated_text,
                                fontsize=10
                            )
                            y_offset += 30
                        except:
                            pass
                    
                    block_index += 1
        
        doc.close()
        
        # 保存输出文档
        output_doc.save(str(output_path))
        output_doc.close()
        
        return output_path
    
    def generate_bilingual_pdf(
        self,
        source_pdf_path: Path,
        translated_blocks: List[Dict[str, str]],
        output_path: Path
    ) -> Path:
        """
        生成双语对照 PDF
        左侧原文，右侧译文
        
        Args:
            source_pdf_path: 原始 PDF 路径
            translated_blocks: [{"original": "...", "translated": "..."}, ...]
            output_path: 输出路径
        """
        doc = fitz.open(str(source_pdf_path))
        output_doc = fitz.open()
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 创建双倍宽度的页面
            new_width = page.rect.width * 2 + 20  # 中间留间隔
            new_height = page.rect.height
            
            new_page = output_doc.new_page(
                width=new_width,
                height=new_height
            )
            
            # 左侧放原文
            new_page.show_pdf_page(
                fitz.Rect(0, 0, page.rect.width, page.rect.height),
                doc,
                page_num
            )
            
            # 中间分隔线
            mid_x = page.rect.width + 10
            new_page.draw_line(
                fitz.Point(mid_x, 20),
                fitz.Point(mid_x, new_height - 20),
                color=(0.8, 0.8, 0.8),
                width=1
            )
            
            # 右侧放译文
            # 提取原页面文本并添加译文
            text_dict = page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:
                    bbox = block.get("bbox")
                    if bbox:
                        # 在右侧对应位置添加译文
                        translated_rect = fitz.Rect(
                            mid_x + 10 + bbox[0],
                            bbox[1],
                            mid_x + 10 + bbox[2],
                            bbox[3]
                        )
                        
                        # 获取原文
                        original_text = ""
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                original_text += span.get("text", "")
                        
                        # 查找对应的译文
                        translated_text = original_text  # 默认使用原文
                        for tb in translated_blocks:
                            if tb.get("original", "").strip() == original_text.strip():
                                translated_text = tb.get("translated", original_text)
                                break
                        
                        try:
                            new_page.insert_textbox(
                                translated_rect,
                                translated_text,
                                fontsize=9,
                                fontname="china-s"
                            )
                        except:
                            pass
        
        doc.close()
        output_doc.save(str(output_path))
        output_doc.close()
        
        return output_path
    
    def generate_overlay_pdf(
        self,
        source_pdf_path: Path,
        page_translations: Dict[int, List[Dict]],
        output_path: Path
    ) -> Path:
        """
        生成覆盖式翻译 PDF - 直接在原位置用译文替换原文
        保留所有图片和公式
        
        Args:
            source_pdf_path: 原始 PDF 路径
            page_translations: {page_num: [{"bbox": (x0,y0,x1,y1), "text": "译文"}, ...]}
            output_path: 输出路径
        """
        doc = fitz.open(str(source_pdf_path))
        
        for page_num, translations in page_translations.items():
            if page_num >= len(doc):
                continue
                
            page = doc[page_num]
            
            for trans in translations:
                bbox = trans.get("bbox")
                text = trans.get("text", "")
                
                if not bbox or not text:
                    continue
                
                rect = fitz.Rect(bbox)
                
                # 用白色矩形覆盖原文
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                
                # 插入译文
                try:
                    page.insert_textbox(
                        rect,
                        text,
                        fontsize=9,
                        fontname="china-s",
                        align=fitz.TEXT_ALIGN_LEFT
                    )
                except:
                    # 尝试使用更小的字体
                    try:
                        page.insert_textbox(
                            rect,
                            text,
                            fontsize=7,
                            fontname="china-s"
                        )
                    except:
                        pass
        
        doc.save(str(output_path))
        doc.close()
        
        return output_path
