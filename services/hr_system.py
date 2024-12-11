from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.vector_stores.kdbai import KDBAIVectorStore
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.response_synthesizers import get_response_synthesizer
import nest_asyncio
from core.models import initialize_models
from core.database import initialize_database
from core.parser import create_parser, parse_documents
import os


@dataclass
class DocumentSource:
    """文件來源追踪"""

    title: str
    section: str
    page: int
    content: str
    file_path: str


class EnhancedHRSystem:
    def __init__(self):
        """初始化系統"""
        # 初始化模型
        self.llm, self.embed_model = initialize_models()

        # 初始化解析器
        self.parser = create_parser()

        # 初始化數據庫
        self.table = initialize_database()

        self.index = None
        self.query_engine = None
        self.document_sources = {}

    def process_pdfs(self, pdf_files: List[str]) -> str:
        """處理PDF文件"""
        try:
            print(f"開始處理文件: {pdf_files}")

            # 解析文檔
            base_nodes, objects, self.document_sources = parse_documents(
                self.parser, self.llm, pdf_files
            )

            print("初始化向量存儲...")
            # 設置向量存儲
            vector_store = KDBAIVectorStore(self.table)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            print("創建索引...")
            # 創建索引
            self.index = VectorStoreIndex(
                nodes=base_nodes + objects, storage_context=storage_context
            )

            print("配置查詢引擎...")
            # 設置查詢引擎
            cohere_rerank = CohereRerank(top_n=10)

            # 使用自定義的響應合成器
            response_synthesizer = get_response_synthesizer(
                response_mode="tree_summarize", use_async=True
            )

            self.query_engine = self.index.as_query_engine(
                similarity_top_k=20,
                node_postprocessors=[cohere_rerank],
                response_synthesizer=response_synthesizer,
                vector_store_kwargs={"index": "flat"},
                verbose=True,
            )

            print("文件處理完成")
            return "文件處理完成！系統已準備就緒。"

        except Exception as e:
            print(f"處理文件時出現錯誤: {str(e)}")
            return f"處理文件時發生錯誤：{str(e)}"

    def get_enhanced_response(
        self, question: str, context_nodes: List[Any]
    ) -> Tuple[str, List[DocumentSource]]:
        """生成增強的回應和來源資訊"""
        prompt = f"""
        作為專業的人力資源顧問，請根據提供的文件內容回答以下問題。
        
        注意事項：
        1. 必須使用繁體中文回答
        2. 使用台灣常見的格式與用語
        3. 不使用 markdown 語法
        4. 標題使用「」作為標示

        問題：{question}

        回答要求：
        1. 回答準確性：
           - 只使用提供的文件內容
           - 提供具體的數字、條件和要求
           - 明確指出法規依據
        
        2. 語境理解：
           - 識別問題的具體情境
           - 提供針對性的規定和說明
           - 避免無關的通用回答
        
        3. 回答完整性：
           - 涵蓋所有相關面向（權利、義務、程序等）
           - 說明申請流程和必要文件
           - 提供相關的配套措施
        
        4. 表達方式：
           - 使用溫和專業的語氣
           - 條理清晰，重點突出
           - 使用台灣常見的行政用語

        格式範例：
        「法規依據」
        一、法規名稱：○○○
        二、修正日期：○○○
        
        「申請條件與流程」
        一、申請時間：○○○
        二、應備文件：○○○

        請基於以下文件內容回答：
        {context_nodes}
        """

        print("生成回答...")
        response = self.llm.complete(prompt)

        print("收集來源...")
        sources = []
        seen_content = set()  # 用於內容去重

        for node in context_nodes:
            if hasattr(node, "metadata"):
                # 只取前 100 字作為內容標識
                content_preview = node.text[:100] if hasattr(node, "text") else ""
                if content_preview not in seen_content:
                    seen_content.add(content_preview)
                    source = DocumentSource(
                        title=self.document_sources.get(
                            node.metadata.get("file_path", ""), {}
                        ).get("title", "未知文件"),
                        section=node.metadata.get("section", "未分類章節"),
                        page=node.metadata.get("page", 0),
                        content=content_preview,
                        file_path=node.metadata.get("file_path", ""),
                    )
                    sources.append(source)

        return str(response), sources

    def ask_question(self, question: str) -> str:
        """處理問題並返回格式化的回答"""
        if not self.query_engine:
            return "請先上傳並處理PDF文件！"

        try:
            print(f"處理問題: {question}")
            retrieval_results = self.query_engine._retriever.retrieve(question)
            context_nodes = [result.node for result in retrieval_results]

            response, sources = self.get_enhanced_response(question, context_nodes)

            formatted_response = response + "\n\n「參考來源」\n"
            seen_sources = set()

            for source in sources:
                source_id = f"{source.title}_{source.section}_{source.page}"
                if source_id not in seen_sources:
                    seen_sources.add(source_id)
                    formatted_response += f"◆ 《{source.title}》"
                    if source.section != "未分類章節":
                        formatted_response += f"【{source.section}】"
                    if source.page > 0:
                        formatted_response += f" 第{source.page}頁"
                    formatted_response += f"\n  相關內容：{source.content}\n"

            return formatted_response

        except Exception as e:
            print(f"回答問題時出現錯誤: {str(e)}")
            return f"回答問題時發生錯誤：{str(e)}"

    def ask_question(self, question: str) -> str:
        """處理問題並返回格式化的回答"""
        if not self.query_engine:
            return "請先上傳並處理PDF文件！"

        try:
            print(f"處理問題: {question}")
            # 獲取相關文件內容
            retrieval_results = self.query_engine._retriever.retrieve(question)
            context_nodes = [result.node for result in retrieval_results]

            # 生成回答和收集來源
            response, sources = self.get_enhanced_response(question, context_nodes)

            # 格式化輸出
            formatted_response = response + "\n\n法規依據：\n"
            seen_sources = set()  # 用於去重

            for source in sources:
                # 創建唯一標識避免重複
                source_id = f"{source.title}_{source.section}_{source.page}"
                if source_id not in seen_sources:
                    seen_sources.add(source_id)
                    formatted_response += f"- 《{source.title}》"
                    if source.section != "Unknown":
                        formatted_response += f" {source.section}"
                    if source.page > 0:
                        formatted_response += f" (第{source.page}頁)"
                    formatted_response += f"\n  相關內容：{source.content[:100]}..."
                    formatted_response += f"\n  文件位置：{source.file_path}\n"

            return formatted_response

        except Exception as e:
            print(f"回答問題時出現錯誤: {str(e)}")
            return f"回答問題時發生錯誤：{str(e)}"
