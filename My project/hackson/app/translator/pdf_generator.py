"""
PDF ������ - ���ɱ���ͼƬ�Ͳ��ֵķ���� PDF
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple

import fitz  # PyMuPDF

class PDFGenerator:
    """PDF ������ - ����ԭʼ���ֺ�ͼƬ"""
    
    def __init__(self):
        # ����ӳ�䣺���� -> ����·��
        self.fonts = {}
        self._register_fonts()
    
    def _register_fonts(self):
        """����ϵͳ�е���������"""
        # ������������·��
        font_candidates = [
            ("simhei", ["C:/Windows/Fonts/simhei.ttf", "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"]),
            ("simsun", ["C:/Windows/Fonts/simsun.ttc", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]),
            ("msyh", ["C:/Windows/Fonts/msyh.ttc"]),
        ]
        
        self.main_font_path = None
        
        for name, paths in font_candidates:
            for path in paths:
                if os.path.exists(path):
                    self.main_font_path = path
                    break
            if self.main_font_path:
                break
                
    def generate_layout_preserved(
        self,
        source_pdf_path: Path,
        translated_pages: List[Dict[int, str]],
        output_path: Path
    ) -> Path:
        """
        ����ԭʼ PDF ���ɷ����� PDF (����ģʽ)
        
        Args:
            source_pdf_path: ԭʼ PDF ·��
            translated_pages: ÿһҳ�ķ������б���
                              List[Dict[block_index, translated_text]]
                              �б�������Ӧҳ��
            output_path: ���·��
            
        Returns:
            ����ļ�·��
        """
        doc = fitz.open(str(source_pdf_path))
        
        # ȷ�����Ŀ¼����
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        for page_idx, page in enumerate(doc):
            if page_idx >= len(translated_pages):
                continue
                
            page_translations = translated_pages[page_idx]
            if not page_translations:
                continue
            
            # ��ȡԭʼ�ı���λ��
            text_dict = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
            blocks = text_dict.get("blocks", [])
            text_blocks = [b for b in blocks if b.get("type") == 0]
            
            # Ϊ��ҳע������
            font_ref = "helv"
            if self.main_font_path:
                try:
                    # ʹ�� fontname="cjk" ��Ϊ����
                    page.insert_font(fontname="cjk", fontfile=self.main_font_path)
                    font_ref = "cjk"
                except Exception:
                    font_ref = "helv"

            for block_idx, text in page_translations.items():
                if block_idx >= len(text_blocks):
                    continue
                
                original_block = text_blocks[block_idx]
                bbox = original_block["bbox"]
                original_text_rect = fitz.Rect(bbox)
                
                # 1. Ϳ��ԭʼ����
                page.draw_rect(original_text_rect, color=(1, 1, 1), fill=(1, 1, 1))
                
                # 2. д�뷭����ı�
                # ��ȡԭ�������С��Ϊ�ο� (ȡ��һ��span)
                origin_size = 9
                try:
                    origin_size = original_block["lines"][0]["spans"][0]["size"]
                except:
                    pass
                
                try:
                    # �����ı�
                    page.insert_textbox(
                        original_text_rect,
                        text,
                        fontsize=origin_size,
                        fontname=font_ref,
                        align=0, # Left
                    )
                except Exception as e:
                    print(f"Error drawing text on page {page_idx} block {block_idx}: {e}")

        doc.save(str(output_path))
        doc.close()
        return output_path
