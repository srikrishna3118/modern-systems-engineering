from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.preprocessing import normalize

from rag.index import RagIndex


@dataclass(frozen=True)
class Retrieved:
    score: float
    source: str
    chunk_id: int
    text: str


def retrieve(index: RagIndex, query: str, *, top_k: int = 5) -> list[Retrieved]:
    q = index.vectorizer.transform([query])
    q = normalize(q, norm="l2", copy=False)

    scores = (index.matrix @ q.T).toarray().ravel()
    if top_k <= 0:
        return []

    best = np.argsort(scores)[::-1][:top_k]
    results: list[Retrieved] = []
    for i in best:
        chunk = index.chunks[int(i)]
        results.append(
            Retrieved(
                score=float(scores[int(i)]),
                source=chunk.source,
                chunk_id=chunk.chunk_id,
                text=chunk.text,
            )
        )
    return results
