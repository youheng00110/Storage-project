"""
Anthropic Claude API 服务实现
"""
import asyncio
from typing import List, Optional

from anthropic import AsyncAnthropic

from .base import BaseAIService, TranslationOptions


class ClaudeService(BaseAIService):
    """Anthropic Claude API 服务"""
    
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        super().__init__(api_key, model or self.DEFAULT_MODEL)
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def translate(
        self, 
        text: str, 
        options: Optional[TranslationOptions] = None
    ) -> str:
        """翻译单段文本"""
        if not text.strip():
            return text
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.get_system_prompt(),
                messages=[
                    {"role": "user", "content": self.get_translation_prompt(text)}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"Claude 翻译失败: {str(e)}")
    
    async def translate_batch(
        self, 
        texts: List[str], 
        options: Optional[TranslationOptions] = None
    ) -> List[str]:
        """批量翻译文本"""
        semaphore = asyncio.Semaphore(3)
        
        async def translate_with_semaphore(text: str) -> str:
            async with semaphore:
                return await self.translate(text, options)
        
        tasks = [translate_with_semaphore(text) for text in texts]
        return await asyncio.gather(*tasks)
