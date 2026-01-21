"""
OpenAI API 服务实现
"""
import asyncio
from typing import List, Optional

from openai import AsyncOpenAI

from .base import BaseAIService, TranslationOptions


class OpenAIService(BaseAIService):
    """OpenAI API 服务"""
    
    DEFAULT_MODEL = "gpt-4o-mini"
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        super().__init__(api_key, model or self.DEFAULT_MODEL)
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def translate(
        self, 
        text: str, 
        options: Optional[TranslationOptions] = None
    ) -> str:
        """翻译单段文本"""
        if not text.strip():
            return text
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": self.get_translation_prompt(text)}
                ],
                temperature=0.3,
                max_tokens=4096
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI 翻译失败: {str(e)}")
    
    async def translate_batch(
        self, 
        texts: List[str], 
        options: Optional[TranslationOptions] = None
    ) -> List[str]:
        """批量翻译文本（并发控制）"""
        semaphore = asyncio.Semaphore(3)  # 限制并发数
        
        async def translate_with_semaphore(text: str) -> str:
            async with semaphore:
                return await self.translate(text, options)
        
        tasks = [translate_with_semaphore(text) for text in texts]
        return await asyncio.gather(*tasks)
