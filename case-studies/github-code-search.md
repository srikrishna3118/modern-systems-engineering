# Case Study: GitHub Code Search

## Overview

GitHub code search answers regular-expression and symbol queries over every public repository it hosts, plus the private repositories a user is allowed to see. The corpus is source code: short identifiers, punctuation, and exact substrings matter more than the word stems a document search engine is built around. The system GitHub described for this product (the Blackbird engine) separates indexing from querying and treats the index as derived data.

## Key Challenges

- **The queries are not keywords.** Developers search for `TODO`, `func main`, or a regex. Dropping punctuation or stemming "running" into "run" would hide the matches they came for.
- **The corpus is duplicated.** The same blob of code appears in millions of forks. Indexing every copy wastes the cluster and complicates deletion.
- **Freshness.** A push should become searchable quickly, without rewriting an index of the whole corpus.
- **Authorization.** A query from a signed-in user must not return a private blob they cannot already see. The index is shared; visibility is not.
- **Fan-out.** A rare trigram still has to be looked up across the shards that might hold it, and the tail of a popular trigram is large.

## Architecture Highlights

- **Content-addressed blobs.** Indexing keys off the blob id. Identical contents are indexed once no matter how many repositories point at them. A push of a fork mostly updates a membership list, not the postings.
- **Code-oriented index.** Blackbird keeps the tokens developers type, including punctuation where it distinguishes syntax, and supports regex by intersecting n-gram postings and then verifying the pattern. This is the same "candidate generation, then verify" shape as typo expansion in a document search engine, with a different candidate key.
- **Separate index and query tiers.** Ingestion turns new blobs into postings. Query nodes serve shards and do not share a fate with the ingestion pipeline, so a big push does not stall searches.
- **Derived index.** Git remains the source of truth. A shard can be rebuilt from blobs. That is what makes a bad deploy recoverable.
- **Access checks outside the postings.** The engine finds candidate blobs; a permission step filters them to what the caller can already open. Keeping permissions out of the postings avoids rewriting the index every time a team changes.

## Technology Stack

- Rust search engine (Blackbird), custom inverted index rather than a general-purpose cluster such as Elasticsearch
- Git blob storage as the source of truth
- Sharded query tier with replicas so one shard failure does not fail the query

## Lessons Learned

1. **Index the thing users type.** A natural-language analyzer is the wrong tool for source code, even though both systems are "search."
2. **Content addressing collapses duplicate work** in a corpus dominated by forks.
3. **Ingestion and query scale on different axes.** Split them so a backlog of pushes degrades freshness, not availability of search.
4. **Authorization is a filter on results, backed by the same rules as the rest of the product,** not a second copy of the ACL inside every posting.
5. **An index you can rebuild is an index you can shard, migrate, and roll back.**

## Where this fits in the curriculum

- [Course 07, Exercise 4: Full-text search](../course-07-advanced-system-design/exercises/04-full-text-search.md) — document search with the same derived-index and fan-out questions, and a different analyzer.
- [Course 07, Lecture 3: Database selection](../course-07-advanced-system-design/lectures/lecture-03-database-selection.md) — when the source of truth and the query store should differ.
- Contrast with [GitHub code review](github-code-review.md), which is the pull-request path, not the index.

## Further Reading

- [GitHub Engineering Blog](https://github.blog/category/engineering/)
- GitHub's public write-up, "The technology behind GitHub's new code search" (2023), describes Blackbird, blob deduplication, and regex over n-grams.
