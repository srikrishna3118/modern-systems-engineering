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
        snippet = r.text.strip().replace("\n", " ")
        print(f"  {snippet[:220]}{'...' if len(snippet) > 220 else ''}")

    # Starter answering: purely extractive.
    # TODO (exercise): add a generation step that composes an answer with citations.
    print("\nAnswer (extractive):")
    if results:
        print(results[0].text.strip()[:600])
    else:
        print("No relevant context found.")


if __name__ == "__main__":
    main()
