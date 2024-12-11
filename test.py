#check UI 介面
# import gradio as gr

# def greet(name):
#     return "Hello " + name + "!"

# demo = gr.Interface(
#     fn=greet,
#     inputs="text",
#     outputs="text",
#     title="測試界面"
# )

# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=8080)

# check 環境變數裡面的keys是否正確

import os
from dotenv import load_dotenv
import sys

def check_env_vars():
    """檢查環境變量的載入狀態"""
    # 獲取當前工作目錄
    current_dir = os.getcwd()
    print(f"\n當前工作目錄: {current_dir}")
    
    # 檢查 .env 文件是否存在
    env_path = os.path.join(current_dir, '.env')
    print(f"\n.env 文件位置: {env_path}")
    print(f".env 文件是否存在: {os.path.exists(env_path)}")
    
    # 嘗試載入 .env
    load_dotenv(override=True)
    
    # 要檢查的環境變量列表
    env_vars = [
        "LLAMA_CLOUD_API_KEY",
        "OPENAI_API_KEY",
        "COHERE_API_KEY",
        "KDBAI_API_KEY",
        "KDBAI_ENDPOINT"
    ]
    
    print("\n環境變量檢查結果:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # 只顯示前4個和後4個字符，中間用***替代
            masked_value = value[:4] + "***" + value[-4:] if len(value) > 8 else "***"
            print(f"{var}: {masked_value}")
        else:
            print(f"{var}: 未設置")

if __name__ == "__main__":
    check_env_vars()