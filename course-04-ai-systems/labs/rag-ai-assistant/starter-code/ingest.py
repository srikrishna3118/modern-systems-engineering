from __future__ import annotations

import argparse

from rag.chunking import chunk_text
from rag.index import Chunk, build_index, save_index
from rag.io import load_documents


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", required=True, help="Directory of .md/.txt docs")
    parser.add_argument("--out", required=True, help="Output path (e.g. data/index.pkl)")
    parser.add_argument("--chunk-size", type=int, default=800)
    parser.add_argument("--overlap", type=int, default=100)
    args = parser.parse_args()

    documents = load_documents(args.docs)
    chunks: list[Chunk] = []
    for doc in documents:
        doc_chunks = chunk_text(doc.text, chunk_size=args.chunk_size, overlap=args.overlap)
        for i, text in enumerate(doc_chunks):
            chunks.append(Chunk(source=doc.source, chunk_id=i, text=text))

    index = build_index(chunks)
    save_index(index, args.out)
    print(f"indexed {len(documents)} docs -> {len(chunks)} chunks")
    print(f"wrote index: {args.out}")


if __name__ == "__main__":
    main()
