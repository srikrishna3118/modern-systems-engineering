from __future__ import annotations

import argparse

from rag.index import load_index
from rag.retrieval import retrieve


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    index = load_index(args.index)
    results = retrieve(index, args.question, top_k=args.top_k)

    print("\nRetrieved context:")
    for r in results:
        print(f"- [{r.source}#{r.chunk_id}] score={r.score:.3f}")

    print("\nAnswer (grounded, with citations):")
    if not results:
        print("No relevant context found.")
        return

    # Simple grounded answer: summarize top passages with citations.
    for r in results[:3]:
        snippet = r.text.strip().replace("\n", " ")
        snippet = snippet[:220] + ("..." if len(snippet) > 220 else "")
        print(f"- {snippet} ({r.source}#{r.chunk_id})")


if __name__ == "__main__":
    main()
