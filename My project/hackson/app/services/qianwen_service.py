"""
通义千问 API 服务实现
"""
import asyncio
from typing import List, Optional
from http import HTTPStatus

import dashscope
from dashscope import Generation

from .base import BaseAIService, TranslationOptions


class QianwenService(BaseAIService):
    """通义千问 API 服务"""
    
    DEFAULT_MODEL = "qwen-turbo"
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        super().__init__(api_key, model or self.DEFAULT_MODEL)
        dashscope.api_key = api_key
    
    async def translate(
        self, 
        text: str, 
        options: Optional[TranslationOptions] = None
    ) -> str:
        """翻译单段文本"""
        if not text.strip():
            return text
        
        try:
            # 使用线程池执行同步 API 调用
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._sync_translate,
                text
            )
            return response
        except Exception as e:
            raise RuntimeError(f"通义千问翻译失败: {str(e)}")
    
    def _sync_translate(self, text: str) -> str:
        """同步翻译方法"""
        response = Generation.call(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": self.get_translation_prompt(text)}
            ],
            temperature=0.3,
            max_tokens=4096,
            result_format='message'
        )
        
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content.strip()
        else:
            raise RuntimeError(
                f"API 错误: {response.code} - {response.message}"
            )
    
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
