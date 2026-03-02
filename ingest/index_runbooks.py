from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.ollama_embed import embed

COLLECTION = "runbooks"

def chunk_text(text: str, chunk_chars: int = 900) -> list[str]:
    text = text.strip()
    out = []
    i = 0
    while i < len(text):
        c = text[i : i + chunk_chars].strip()
        if c:
            out.append(c)
        i += chunk_chars
    return out

def main() -> None:
    client = QdrantClient(url="http://localhost:6333")

    dim = len(embed("dim check"))

    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )

    runbook_dir = Path("data/runbooks")
    points = []
    pid = 1

    for fp in runbook_dir.glob("*.txt"):
        doc_id = fp.stem
        raw = fp.read_text(encoding="utf-8")
        for idx, chunk in enumerate(chunk_text(raw)):
            vec = embed(chunk)
            chunk_id = f"{doc_id}_c{idx}"
            points.append(
                PointStruct(
                    id=pid,
                    vector=vec,
                    payload={"doc_id": doc_id, "chunk_id": chunk_id, "text": chunk},
                )
            )
            pid += 1

    if points:
        client.upsert(collection_name=COLLECTION, points=points)

    print("Indexed chunks:", len(points))

if __name__ == "__main__":
    main()