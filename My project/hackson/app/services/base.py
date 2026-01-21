"""
AI 服务基类接口
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class TranslationOptions:
    """翻译选项"""
    source_lang: str = "en"
    target_lang: str = "zh"
    style: str = "academic"  # academic, casual, technical
    preserve_formatting: bool = True


class BaseAIService(ABC):
    """AI 服务基类"""
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def translate(
        self, 
        text: str, 
        options: Optional[TranslationOptions] = None
    ) -> str:
        """翻译单段文本"""
        pass
    
    @abstractmethod
    async def translate_batch(
        self, 
        texts: List[str], 
        options: Optional[TranslationOptions] = None
    ) -> List[str]:
        """批量翻译文本"""
        pass
    
    def get_system_prompt(self) -> str:
        """获取学术翻译系统提示词"""
        return """你是一名专业的学术论文翻译专家。请严格遵守以下规则翻译：

1. 结构保留：
   - 保持所有标题、章节编号、列表格式
   - 保留空行和段落分隔
   
2. 不翻译内容（保持原样）：
   - LaTeX 数学公式（如 $...$ 或 $$...$$）
   - 引用编号（如 [1], [2]）
   - 代码块
   - 图表标识符（如 Figure 1, Table 2）
   - 参考文献中的论文标题、作者名、期刊名
   
3. 翻译风格：
   - 使用正式的学术中文
   - 保持术语一致性
   - 专有名词首次出现时保留英文原文并加中文注释
   
4. 输出格式：
   - 仅返回翻译后的文本
   - 不添加任何解释、评论或额外标记"""
    
    def get_translation_prompt(self, text: str) -> str:
        """生成翻译提示词"""
        return f"""请将以下英文学术文本翻译成中文：

{text}

翻译："""
