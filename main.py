import os
import gradio as gr
import nest_asyncio
from dotenv import load_dotenv
from services.hr_system import EnhancedHRSystem

class HRInterface:
    def __init__(self):
        # 清除舊環境變量並重新載入
        self.clear_and_reload_env()
        self.system = None
        
    def clear_and_reload_env(self):
        """清除並重新載入環境變量"""
        env_vars = [
            "LLAMA_CLOUD_API_KEY",
            "OPENAI_API_KEY",
            "COHERE_API_KEY",
            "KDBAI_API_KEY",
            "KDBAI_ENDPOINT"
        ]
        
        # 清除舊環境變量
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
        
        # 重新載入環境變量
        load_dotenv(override=True)
        
        # 驗證環境變量
        print("\n使用中的環境變量:")
        missing_vars = []
        for var in env_vars:
            value = os.getenv(var)
            if value:
                masked_value = value[:4] + "***" + value[-4:] if len(value) > 8 else "***"
                print(f"{var}: {masked_value}")
            else:
                missing_vars.append(var)
                print(f"{var}: 未設置")
        
        if missing_vars:
            raise ValueError(f"缺少必要的環境變量: {', '.join(missing_vars)}")

    def init_system(self):
        """初始化系統"""
        try:
            self.system = EnhancedHRSystem()
            return "系統初始化成功！請上傳PDF文件。"
        except Exception as e:
            return f"初始化失敗：{str(e)}"

    def process_files(self, files):
        """處理上傳的文件"""
        if not self.system:
            return "請先初始化系統！"
        if not files:
            return "請選擇文件！"
        file_paths = [f.name for f in files]
        return self.system.process_pdfs(file_paths)

    def ask_question(self, question):
        """處理用戶提問"""
        if not self.system:
            return "請先初始化系統！"
        if not question:
            return "請輸入問題！"
        return self.system.ask_question(question)

def create_interface():
    """創建 Gradio 界面"""
    try:
        hr_interface = HRInterface()
    except Exception as e:
        print(f"初始化失敗：{str(e)}")
        return None

    with gr.Blocks(title="智能人資顧問系統") as demo:
        gr.Markdown("# 智能人資顧問系統")
        
        with gr.Tab("系統控制"):
            init_btn = gr.Button("初始化系統")
            init_output = gr.Textbox(label="系統狀態")
            
            upload_box = gr.File(
                label="上傳PDF文件",
                file_count="multiple"
            )
            process_btn = gr.Button("處理文件")
            process_output = gr.Textbox(label="處理結果")

        with gr.Tab("諮詢系統"):
            input_box = gr.Textbox(
                label="問題輸入",
                placeholder="請輸入您的問題...",
                lines=3
            )
            submit_btn = gr.Button("送出問題")
            output_box = gr.Textbox(label="回答內容", lines=8)

        init_btn.click(
            hr_interface.init_system,
            outputs=init_output
        )
        process_btn.click(
            hr_interface.process_files,
            inputs=upload_box,
            outputs=process_output
        )
        submit_btn.click(
            hr_interface.ask_question,
            inputs=input_box,
            outputs=output_box
        )

    return demo

def main():
    """主程序入口"""
    # 在開發環境中使用 nest_asyncio
    nest_asyncio.apply()
    
    # 創建界面
    demo = create_interface()
    if demo is None:
        return
    
    # 啟動配置
    launch_kwargs = {
        "server_name": "127.0.0.1",  # 本地主機
        "server_port": 8080,         # 使用 8080 端口
        "show_error": True,          # 顯示錯誤信息
        "debug": True                # 開啟調試模式
    }
    
    # 啟動界面
    try:
        demo.launch(**launch_kwargs)
    except Exception as e:
        print(f"啟動失敗：{str(e)}")

if __name__ == "__main__":
    main()