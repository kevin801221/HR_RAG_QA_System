from llama_parse import LlamaParse
from llama_index.core.node_parser import MarkdownElementNodeParser
from typing import List, Tuple
from llama_index.core import Document
import os

def create_parser():
    """創建文檔解析器"""
    parsing_instructions = """
    這是人力資源法規文件，請特別注意：
    1. 精確擷取所有法規條文和數字要求（如請假天數、薪資計算等）
    2. 保留完整的章節結構和條文編號
    3. 標記所有關鍵定義、權利義務和程序要求
    4. 特別注意特殊情況的規定（如颱風假、性騷擾防治等）
    5. 提取所有申請流程、期限和必要文件的要求
    6. 確保保留每個段落的頁碼和章節資訊
    """
    
    return LlamaParse(
        result_type="markdown",
        parsing_instructions=parsing_instructions
    )

def parse_documents(parser: LlamaParse, llm, pdf_files: List[str]) -> Tuple[List, List, dict]:
    """解析文檔並返回節點和文件來源信息"""
    documents = []
    document_sources = {}
    
    for pdf_file in pdf_files:
        print(f"處理文件: {pdf_file}")
        file_name = os.path.basename(pdf_file)
        
        # 使用 LlamaParse 解析文檔
        parsed_docs = parser.load_data(pdf_file)
        
        # 添加 metadata 到每個文檔
        for idx, doc in enumerate(parsed_docs):
            # 從文檔內容中提取章節信息（這裡需要根據實際文檔格式調整）
            section = extract_section(doc.text) if hasattr(doc, 'text') else f'第{idx + 1}節'
            
            doc.metadata = {
                'file_name': file_name,
                'file_path': pdf_file,
                'page': idx + 1,
                'section': section
            }
            documents.append(doc)
        
        # 存儲文件來源信息
        document_sources[pdf_file] = {
            'title': file_name,
            'path': pdf_file
        }
    
    # 使用 MarkdownElementNodeParser 處理文檔
    node_parser = MarkdownElementNodeParser(
        llm=llm,
        num_workers=1,
        include_metadata=True
    )
    
    # 獲取並處理節點
    nodes = node_parser.get_nodes_from_documents(documents)
    base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
    
    # 確保所有節點都有完整的 metadata
    for node in base_nodes + objects:
        if not hasattr(node, 'metadata'):
            node.metadata = {}
        if 'file_path' not in node.metadata:
            node.metadata['file_path'] = node.metadata.get('file_name', '')
        if 'section' not in node.metadata:
            node.metadata['section'] = '未分類章節'
        if 'page' not in node.metadata:
            node.metadata['page'] = 0
    
    return base_nodes, objects, document_sources

def extract_section(text: str) -> str:
    """從文本中提取章節信息"""
    # 這裡可以根據實際文檔格式添加更複雜的章節提取邏輯
    # 目前使用簡單的實現
    lines = text.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ['章', '節', '條']):
            return line.strip()
    return '未分類章節'