"""
LaTeX 生成器 - 将提取的内容和翻译结果生成 LaTeX 项目并编译为 PDF
"""
import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any, Tuple
from app.parsers.pdf_parser import ParsedDocument, ImageInfo

class LatexGenerator:
    """LaTeX 生成器"""
    
    def __init__(self):
        pass
        
    def generate(
        self,
        document: ParsedDocument,
        translated_pages: List[Dict[int, str]],
        output_path: Path
    ) -> Path:
        """
        生成 LaTeX 项目并编译
        
        Args:
            document: 解析后的文档对象 (包含图片和元数据)
            translated_pages: 翻译后的文本块映射 List[Dict[block_idx, text]]
            output_path: 最终 PDF 输出路径
            
        Returns:
            生成的 PDF 路径 (如果编译失败，可能返回 None 或抛出异常)
        """
        # 创建临时构建目录
        build_dir = output_path.parent / f"tex_build_{output_path.stem}"
        if build_dir.exists():
            shutil.rmtree(build_dir)
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 保存图片
        images_dir = build_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # 映射图片对象 ID 到文件名
        image_filename_map = {}
        
        # 保存所有页面提取的图片
        for img_idx, img in enumerate(document.images):
            # 简单的命名策略
            img_filename = f"img_{img_idx}.{img.ext}"
            img_path = images_dir / img_filename
            with open(img_path, "wb") as f:
                f.write(img.data)
            image_filename_map[id(img)] = f"images/{img_filename}"
            
        # 2. 生成 tex 内容
        tex_content = self._build_tex_content(document, translated_pages, image_filename_map)
        
        tex_file = build_dir / "main.tex"
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(tex_content)
            
        # 3. 编译 PDF
        try:
            # 假设系统安装了 xelatex
            # 需要编译两次以确保引用正确 (虽然这里主要用绝对定位，一次可能够，但保险起见)
            cmd = ["xelatex", "-interaction=nonstopmode", "main.tex"]
            
            # 第一次编译
            subprocess.run(cmd, cwd=str(build_dir), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 第二次编译 (如果有目录或交叉引用需要)
            # subprocess.run(cmd, cwd=str(build_dir), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            built_pdf = build_dir / "main.pdf"
            if built_pdf.exists():
                shutil.copy(built_pdf, output_path)
                return output_path
            else:
                raise RuntimeError("PDF compilation failed: Output file not found.")
                
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # 如果编译失败，或者没有 xelatex
            print(f"LaTeX compilation failed: {e}")
            
            # 打包整个构建目录 (包含图片和 tex) 供用户下载
            # base_name 不带后缀，root_dir 是要打包的目录
            zip_base_name = str(output_path.with_suffix(""))
            archive_path = shutil.make_archive(zip_base_name, 'zip', build_dir)
            zip_filename = Path(archive_path).name
            
            # 同时也保存一份单独的 tex 文件方便查看
            shutil.copy(tex_file, output_path.with_suffix(".tex"))
            
            raise RuntimeError(
                f"本地 PDF 编译失败。已生成源码包 {zip_filename} 和 .tex 文件。\n"
                f"解决方法 1: 安装 MiKTeX (Windows) 或 TeXLive 并确保 xelatex 在 PATH 中。\n"
                f"解决方法 2: 下载该 zip 包上传到 Overleaf.com 进行在线编译。"
            )
            
        return output_path

    def _build_tex_content(
        self, 
        document: ParsedDocument, 
        translated_pages: List[Dict[int, str]],
        image_filename_map: Dict[int, str]
    ) -> str:
        """构建 LaTeX 源码"""
        
        # LaTeX 头部
        c = []
        c.append(r"\documentclass{article}")
        c.append(r"\usepackage[paperwidth=595pt,paperheight=842pt,margin=0cm]{geometry}") # A4 size default, usually fitz gives pts
        # PyMuPDF 默认单位是 pt (1/72 inch). A4 is 595.27 x 841.89
        # 我们可以针对每页动态设置 geometry，但 article通常全文档一致。
        # 为了极简 hack，这里假设大部分是 A4。或者我们可以用 \usepackage[absolute]{textpos} 忽略页边距。
        
        c.append(r"\usepackage{xeCJK}")
        c.append(r"\setCJKmainfont{SimSun}") # 假设有宋体，或者让用户配置
        c.append(r"\setCJKsansfont{SimHei}")
        c.append(r"\usepackage{graphicx}")
        c.append(r"\usepackage[absolute,overlay]{textpos}")
        c.append(r"\usepackage{calc}")
        c.append(r"\usepackage{color}")
        
        # 设置 textpos 单位为 pt
        c.append(r"\setlength{\TPHorizModule}{1pt}")
        c.append(r"\setlength{\TPVertModule}{1pt}")
        c.append(r"\textblockorigin{0pt}{0pt}") # 原点左上角
        
        c.append(r"\pagestyle{empty}") # 不显示页码，因为我们是还在原排版的
        
        c.append(r"\begin{document}")
        
        for page_idx, page_content in enumerate(document.pages_content):
            # 获取页面尺寸，调整 geometry (如果文档页面大小不一，这比较麻烦，简单的做法是只用 textpos 铺满)
            # LaTeX 很难中途改变页面大小，除非用 pdfpages 或 geometry \newgeometry
            # 这里简单起见，假设页面尺寸固定，或者我们只管内容放置。
            
            # 处理这一页的图片
            for img in page_content.images:
                # img: ImageInfo
                img_path = image_filename_map.get(id(img))
                if not img_path:
                    continue
                
                # 放置图片
                x, y, x1, y1 = img.bbox
                w = x1 - x
                h = y1 - y
                
                # 使用 textblock 放置图片
                # \begin{textblock*}{width}(x,y)
                c.append(f"\\begin{{textblock*}}{{{w}pt}}({x}pt,{y}pt)")
                c.append(f"\\includegraphics[width={w}pt,height={h}pt]{{{img_path}}}")
                c.append(r"\end{textblock*}")
            
            # 处理这一页的文本
            # 需要先找到该页的翻译结果
            translations = {}
            if page_idx < len(translated_pages):
                translations = translated_pages[page_idx]
                
            for b_idx, block in enumerate(page_content.text_blocks):
                x, y, x1, y1 = block["bbox"]
                w = x1 - x
                
                text = translations.get(b_idx, "")
                is_translated = True
                
                # 如果没在 translations 里 (例如公式或者过滤掉的短文本)，使用原文
                if not text:
                     text = block.get("text", "").strip()
                     is_translated = False
                
                if text:
                    # 简单的公式检测，决定是否转义
                    is_formula = False
                    if not is_translated:
                        # 检查是否看起来像 LaTeX 公式
                        if text.startswith("$") or text.startswith("\\") or "equation" in text:
                            is_formula = True
                    
                    if is_formula:
                        # 公式不转义 (可能存在风险，但在 hackson 项目中可接受)
                        safe_text = text
                    else:
                        # 普通文本转义
                        safe_text = self._escape_latex(text)
                    
                    c.append(f"\\begin{{textblock*}}{{{w}pt}}({x}pt,{y}pt)")
                    # 设置字体大小
                    c.append(r"\fontsize{9pt}{11pt}\selectfont") 
                    c.append(f"{safe_text}")
                    c.append(r"\end{textblock*}")
            
            # 换页
            if page_idx < len(document.pages_content) - 1:
                c.append(r"\newpage")
                
        c.append(r"\end{document}")
        return "\n".join(c)

    def _escape_latex(self, text: str) -> str:
        """转义 LaTeX 特殊字符"""
        chars = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "\\": r"\textbackslash{}",
        }
        pattern = re.compile('|'.join(re.escape(k) for k in chars.keys()))
        return pattern.sub(lambda m: chars[m.group()], text)

import re
