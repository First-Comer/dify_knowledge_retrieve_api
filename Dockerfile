FROM langgenius/dify-api:1.3.1

COPY ../api /app/api
COPY ../api/core/workflow/nodes/knowledge_retrieval/knowledge_retrieval_node.py /app/api/core/workflow/nodes/knowledge_retrieval/knowledge_retrieval_node.py
