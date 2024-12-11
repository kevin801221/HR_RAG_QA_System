from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from config.settings import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    EMBEDDING_MODEL,
    GENERATION_MODEL,
)


def initialize_models():
    """初始化所有需要的模型"""
    # 初始化 LLM
    llm = OpenAI(
        model=GENERATION_MODEL,
        temperature=0.1,
        api_key=OPENAI_API_KEY,
        api_base=OPENAI_API_BASE,
    )

    # 初始化 embedding model
    embed_model = OpenAIEmbedding(
        model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY, api_base=OPENAI_API_BASE
    )

    # 設置全局配置
    Settings.llm = llm
    Settings.embed_model = embed_model

    return llm, embed_model
