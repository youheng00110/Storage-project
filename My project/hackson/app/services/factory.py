"""
AI 服务工厂
"""
from typing import Optional

from .base import BaseAIService
from .openai_service import OpenAIService
from .qianwen_service import QianwenService
from .claude_service import ClaudeService
from .modelscope_service import ModelScopeService


def create_ai_service(
    provider: str, 
    api_key: str, 
    model: Optional[str] = None
) -> BaseAIService:
    """
    创建 AI 服务实例
    
    Args:
        provider: 服务提供商 (openai, qianwen, claude, modelscope)
        api_key: API 密钥
        model: 可选的模型名称
    
    Returns:
        BaseAIService: AI 服务实例
    """
    providers = {
        "openai": OpenAIService,
        "qianwen": QianwenService,
        "claude": ClaudeService,
        "modelscope": ModelScopeService,
    }
    
    if provider not in providers:
        raise ValueError(
            f"不支持的 AI 服务提供商: {provider}。"
            f"支持的提供商: {', '.join(providers.keys())}"
        )
    
    return providers[provider](api_key, model)


# 各服务商可用的模型列表
AVAILABLE_MODELS = {
    "openai": [
        {"id": "gpt-4o", "name": "GPT-4o (推荐)"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini (快速)"},
        {"id": "gpt-4-turbo", "name": "GPT-4 Turbo"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo (经济)"},
    ],
    "qianwen": [
        {"id": "qwen-max", "name": "通义千问 Max (推荐)"},
        {"id": "qwen-plus", "name": "通义千问 Plus"},
        {"id": "qwen-turbo", "name": "通义千问 Turbo (快速)"},
    ],
    "claude": [
        {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet (推荐)"},
        {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus (高质量)"},
        {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku (快速)"},
    ],
    "modelscope": [
        {"id": "Qwen/Qwen2.5-72B-Instruct", "name": "Qwen2.5-72B (推荐)"},
        {"id": "Qwen/Qwen2.5-32B-Instruct", "name": "Qwen2.5-32B"},
        {"id": "Qwen/Qwen2.5-Coder-32B-Instruct", "name": "Qwen2.5-Coder-32B"},
        {"id": "Qwen/Qwen2.5-14B-Instruct", "name": "Qwen2.5-14B (快速)"},
    ],
}
