from dataclasses import dataclass


@dataclass
class ChatCompletionConfig:
    model: str
    temperature: int
    n: int
    stream: bool
    stop: str
    max_tokens: int
    presence_penalty: int
    frequency_penalty: int


@dataclass
class ImageConfig:
    n: int
    size: str


@dataclass
class Config:
    chatCompletionConfig: ChatCompletionConfig
    imageConfig: ImageConfig
    max_context_size: int
    auto_modify_cons: bool
    openai_key: str


__all__ = [
    "ChatCompletionConfig",
    "ImageConfig",
    "Config"
]
