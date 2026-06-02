from __future__ import annotations

import pickle
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


@dataclass
class Chunk:
    source: str
    chunk_id: int
    text: str


@dataclass
class RagIndex:
    vectorizer: TfidfVectorizer
    matrix: np.ndarray
    chunks: list[Chunk]


def build_index(chunks: list[Chunk]) -> RagIndex:
    texts = [c.text for c in chunks]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)
    matrix = normalize(matrix, norm="l2", copy=False)
    return RagIndex(vectorizer=vectorizer, matrix=matrix, chunks=chunks)


def save_index(index: RagIndex, out_path: str) -> None:
    with open(out_path, "wb") as f:
        pickle.dump(index, f)


def load_index(path: str) -> RagIndex:
    with open(path, "rb") as f:
        return pickle.load(f)
