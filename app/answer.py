from app.retrieve import retrieve
from app.ollama_llm import generate

import re

def extract_bracket_citations(text: str) -> set[str]:
    return set(re.findall(r"\[([A-Za-z0-9_]+)\]", text))

RULES = """
You are an incident triage assistant.

Rules
1 Use only the provided context as evidence
2 Every action or root cause claim must include a citation like [chunk_id]
3 If evidence is weak, write INSUFFICIENT EVIDENCE and ask for missing logs or metrics
4 Do not invent commands unless they appear in the context
"""

def build_prompt(incident_text: str, contexts: list[dict]) -> str:
    ctx_lines = []
    for c in contexts:
        ctx_lines.append(f"CHUNK {c['chunk_id']}\n{c['text']}\n")
    ctx = "\n".join(ctx_lines)

    return f"""{RULES}

Context
{ctx}

Incident
{incident_text}

Output format
A Hypotheses ranked
B Next actions numbered
C Missing info questions
D Confidence low medium high with one sentence reason
"""

def answer_incident(incident_text: str) -> dict:
    contexts = retrieve(incident_text, k=5)
    prompt = build_prompt(incident_text, contexts)
    resp = generate(prompt)
    return {"answer": resp, "retrieved": contexts}