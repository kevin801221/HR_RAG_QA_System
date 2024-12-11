def __init__(self):
    # 驗證 API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API Key not found in environment variables")
    
    print(f"Using OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:8]}...")  # 驗證使用的是正確的 key
    
    # 其餘初始化code...