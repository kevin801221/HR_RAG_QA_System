import os
from dotenv import load_dotenv

# 載入環境變量
load_dotenv()

# API Keys 配置
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
KDBAI_API_KEY = os.getenv("KDBAI_API_KEY")
KDBAI_ENDPOINT = os.getenv("KDBAI_ENDPOINT")

# OpenAI 配置
OPENAI_API_BASE = "https://api.openai.com/v1"
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4-turbo-preview"

# KDB.AI 配置
KDBAI_TABLE_NAME = "LlamaParse_Table"

# 向量維度配置
EMBEDDING_DIMS = 1536
