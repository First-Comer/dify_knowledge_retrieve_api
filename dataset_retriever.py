# api/services/workflow/dataset_retriever.py

from core.workflow.nodes.knowledge_retrieval.knowledge_retrieval_node import KnowledgeRetrievalNode
from core.workflow.nodes.knowledge_retrieval.entities import KnowledgeRetrievalNodeData
from core.variables import StringSegment

def fetch_dataset_retriever(payload: dict) -> list[dict]:
    # 1. 从 payload 中单独提取 id，剩余字段给 Pydantic
    raw = payload["node_data"].copy()
    node_id = raw.pop("id")
    node_data = KnowledgeRetrievalNodeData(**raw)

    # 2. 提取 query
    selector = node_data.query_variable_selector[0]
    query_str = payload["inputs"][selector]
    if not isinstance(query_str, str):
        raise ValueError("Query must be a string")

    # 3. 初始化 node
    node = KnowledgeRetrievalNode.__new__(KnowledgeRetrievalNode)
    node.id = node_id
    node.node_data = node_data

    # 4. 模拟 runtime state
    class DummyPool:
        def __init__(self, value): self.value = value
        def get(self, _): return StringSegment(self.value)

    class DummyRuntime:
        variable_pool = DummyPool(query_str)

    setattr(node, "graph_runtime_state", DummyRuntime())
    setattr(node, f"graph_{node.id}_runtime_state", DummyRuntime())

    # 5. 补齐其他必需属性
    node.tenant_id = payload["tenant_id"]
    node.user_id = payload["user_id"]
    node.app_id = payload["app_id"]
    node.user_from = type("UserFrom", (), {"value": payload.get("user_from", "api")})()

    # 6. 调用底层检索方法
    results = node._fetch_dataset_retriever(node_data=node_data, query=query_str)

    # 7. 转成 JSON-serializable 的 list[dict]
    out: list[dict] = []
    for r in results:
        try:
            out.append(dict(r))
        except Exception:
            out.append(r)
    return out
