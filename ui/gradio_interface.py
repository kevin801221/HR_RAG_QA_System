import gradio as gr
from services.hr_system import EnhancedHRSystem

def create_gradio_interface():
    """創建 Gradio 界面"""
    system = None
    
    def init_system():
        nonlocal system
        try:
            system = EnhancedHRSystem()
            return "系統初始化成功！請上傳PDF文件。"
        except Exception as e:
            return f"初始化失敗：{str(e)}"
    
    def process_files(files):
        if not system:
            return "請先初始化系統！"
        file_paths = [f.name for f in files]
        return system.process_pdfs(file_paths)
    
    def ask(question):
        if not system:
            return "請先初始化系統！"
        return system.ask_question(question)

    # 創建簡單的界面布局
    with gr.Blocks() as demo:
        gr.Markdown("""
        # 智能人資顧問系統
        提供準確、完整且人性化的人資法規諮詢服務
        """)
        
        # 系統設置頁面
        with gr.Tab("系統設置"):
            init_btn = gr.Button("初始化系統")
            init_output = gr.Textbox(label="系統狀態")
            
            file_input = gr.File(label="上傳PDF文件", file_count="multiple")
            process_btn = gr.Button("處理文件")
            process_output = gr.Textbox(label="處理狀態")
        
        # 諮詢系統頁面
        with gr.Tab("諮詢系統"):
            question = gr.Textbox(
                label="請輸入您的問題",
                placeholder="例如：請問特休假如何計算？",
                lines=3
            )
            ask_btn = gr.Button("提問")
            answer = gr.Textbox(label="回答", lines=10)
        
        # 設置事件處理
        init_btn.click(init_system, outputs=init_output)
        process_btn.click(process_files, inputs=file_input, outputs=process_output)
        ask_btn.click(ask, inputs=question, outputs=answer)

    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(debug=True)