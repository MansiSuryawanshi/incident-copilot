from qdrant_client import QdrantClient
from app.ollama_embed import embed

COLLECTION = "runbooks"

def retrieve(query: str, k: int = 5) -> list[dict]:
    client = QdrantClient(url="http://localhost:6333")
    qv = embed(query)

    # This works across current client versions
    res = client.query_points(
        collection_name=COLLECTION,
        query=qv,
        limit=k,
        with_payload=True,
    )

    out = []
    for p in res.points:
        payload = p.payload or {}
        out.append(
            {
                "doc_id": payload.get("doc_id"),
                "chunk_id": payload.get("chunk_id"),
                "text": payload.get("text", ""),
                "score": float(p.score) if p.score is not None else None,
            }
        )
    return out