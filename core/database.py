import kdbai_client as kdbai
from config.settings import (
    KDBAI_API_KEY,
    KDBAI_ENDPOINT,
    KDBAI_TABLE_NAME,
    EMBEDDING_DIMS,
)


def initialize_database():
    """初始化並設置 KDB.AI 數據庫"""
    # 連接到 KDB.AI
    session = kdbai.Session(api_key=KDBAI_API_KEY, endpoint=KDBAI_ENDPOINT)
    db = session.database("default")

    # 定義 schema
    schema = [
        dict(name="document_id", type="bytes"),
        dict(name="text", type="bytes"),
        dict(name="embeddings", type="float32s"),
    ]

    # 定義索引
    indexFlat = {
        "name": "flat",
        "type": "flat",
        "column": "embeddings",
        "params": {"dims": EMBEDDING_DIMS, "metric": "L2"},
    }

    # 確保表不存在
    try:
        db.table(KDBAI_TABLE_NAME).drop()
    except kdbai.KDBAIException:
        pass

    # 創建表
    table = db.create_table(KDBAI_TABLE_NAME, schema, indexes=[indexFlat])

    return table
