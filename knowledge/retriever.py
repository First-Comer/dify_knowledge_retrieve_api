# api/controllers/console/knowledge/retriever.py

from flask_restful import Resource, request
from services.workflow.dataset_retriever import fetch_dataset_retriever

class KnowledgeRetrieverApi(Resource):
    def post(self):
        payload = request.get_json(force=True)
        result = fetch_dataset_retriever(payload)
        return {"status": "success", "data": result}, 200
