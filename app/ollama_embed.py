import requests

OLLAMA_URL = "http://localhost:11434"

def embed(text: str) -> list[float]:
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["embedding"]