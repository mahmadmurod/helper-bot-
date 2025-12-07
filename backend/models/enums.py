"""
to be implemented at a latter time 
"""

from enum import Enum

class AIProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"
    MOCK = "mock"