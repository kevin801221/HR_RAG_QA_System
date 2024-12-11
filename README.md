# 智能人資顧問系統 (Intelligent HR Consultant System)

基於 LLM 的智能人力資源法規諮詢系統，整合了 KDB.AI 向量數據庫、Cohere 重排序和 Gradio 介面，提供高效的文件處理和精確的法規諮詢服務。

## 環境需求
可以先創立虛擬環境 python -m venv venv
source ./venv/bin/activate
### Requirements.txt
```txt
llama-index
llama-index-core
llama-index-embeddings-openai
llama-parse
llama-index-vector-stores-kdbai
pandas
llama-index-postprocessor-cohere-rerank
kdbai_client
langchain-openai
openai
httpx
gradio
nest-asyncio
python-dotenv
```

command 安裝所有需要的packages
```bash
pip install -r requirements.txt
```
## 環境變量配置

創建 `.env` 文件，需要包含以下配置：
```env
LLAMA_CLOUD_API_KEY=your_llama_cloud_key
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
KDBAI_ENDPOINT=your_kdbai_endpoint
KDBAI_API_KEY=your_kdbai_key
```

## 系統架構

### 核心組件
- **文檔解析**: LlamaParse
- **向量存儲**: KDB.AI
- **檢索重排**: Cohere Rerank
- **語言模型**: OpenAI GPT-4
- **嵌入模型**: OpenAI Embedding
- **使用者介面**: Gradio

## 部署注意事項

### 代碼重複與整合建議

1. **模型初始化重複**:
   - 發現多處 OpenAI 和 Embedding 模型的初始化代碼
   - 建議統一在一個配置類中初始化

2. **環境變量設置**:
   - 目前分散在多處直接設置
   - 建議統一使用 python-dotenv 載入

3. **數據庫連接**:
   - KDB.AI 的設置與一般查詢引擎有重複
   - 建議統一數據庫連接管理

### 建議專案結構
```
project/
├── .env                    # 環境變量配置
├── .env.example           # 環境變量範例
├── requirements.txt       # 依賴包列表
├── main.py               # 主程序入口
├── config/
│   ├── __init__.py
│   └── settings.py       # 統一配置管理
├── core/
│   ├── __init__.py
│   ├── models.py        # 模型初始化
│   ├── database.py      # 數據庫管理
│   └── parser.py        # 文檔解析
├── services/
│   ├── __init__.py
│   └── hr_system.py     # 核心業務邏輯
└── ui/
    ├── __init__.py
    └── gradio_interface.py # UI 實現
```

## 使用方法

### 1. 系統初始化
```bash
# 1. 安裝主要包
pip install -r requirements.txt

# 2. 配置環境變量
cp .env.example .env
# 編輯 .env 文件填入所需的 API keys
```

### 2. 啟動系統
```bash
python main.py
```
    
### 3. 使用介面

系統提供兩個主要頁面：

#### 系統設置頁面
1. 輸入 OpenAI API Key
2. 初始化系統
3. 上傳 PDF 文件（支援多選）
4. 等待文件處理完成

#### 諮詢系統頁面
1. 輸入問題
2. 獲取智能回答及法規依據

### 4.啟動後的使用流程：

    打開 Gradio 介面後，進入「系統設置」頁面
    點擊「初始化系統」按鈕
    上傳你的 PDF 文件（可以是人資相關的規章制度、法規等）
    點擊「處理文件」按鈕，等待系統處理完成
    切換到「諮詢系統」頁面
    開始輸入問題進行諮詢

    系統會：

    解析上傳的 PDF 文件
    將內容向量化存入 KDB.AI
    使用 Cohere 進行重排序
    透過 GPT-4 生成回答
    
## 性能優化建議

1. **異步處理**:
   - 目前使用 `nest_asyncio.apply()`
   - 建議在生產環境使用正確的異步設計

2. **數據庫優化**:
   - 考慮使用連接池
   - 實現緩存機制

3. **文件處理優化**:
   - 實現分批處理大型文件
   - 添加進度顯示

## 安全性建議

1. **API Key 管理**:
   - 使用環境變量
   - 實現 Key 輪換機制

2. **數據保護**:
   - 實現數據加密存儲
   - 添加訪問控制
### 測試結果截圖，可以設置基本系統初始化和上傳多個PDF文件進行RAG準備。

![image](https://github.com/user-attachments/assets/2767bb48-67fb-46e8-a5aa-f41b02c4a528)

### 檢索之後畫面
![image](https://github.com/user-attachments/assets/43e0af14-21b8-4481-92db-82c19a475c3d)

## License

Apache2.0 License

## 貢獻指南

歡迎提交 Issue 和 Pull Request 來改善系統。
