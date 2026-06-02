# Case Study: GitHub Code Review at Scale

## Overview

GitHub hosts over 200 million repositories and processes millions of pull requests daily. Its code review system is the backbone of collaborative software development, enabling distributed teams to maintain code quality, enforce standards, and ship reliable software. This case study examines the engineering behind GitHub's pull request and code review infrastructure.

## Key Challenges

- **Scale**: Millions of pull requests opened daily, each requiring diff computation, status checks, and notifications
- **Diff Performance**: Computing and rendering diffs for repositories with millions of files and deep commit histories
- **Merge Conflicts**: Detecting and presenting merge conflicts in near-real-time as branches diverge
- **CI/CD Integration**: Orchestrating thousands of status checks per minute across external and internal CI systems
- **Global Availability**: Maintaining low-latency access for developers worldwide

## Architecture Highlights

- **Spokes (Git Storage)**: GitHub's distributed Git storage system uses 3-replica architecture for durability
- **Diff Service**: Computes file-level diffs using optimized libgit2; caches large diffs asynchronously
- **Pull Request Merge Engine**: Implements merge commit, squash, rebase, and sequential merge queue strategies
- **CODEOWNERS Engine**: Maps changed files to required reviewers; enforces review requirements
- **Status Checks Aggregator**: Manages CI integration; prevents merging without required checks

## Technology Stack

- Ruby (Rails), Go (performance-critical services)
- MySQL (Vitess sharded), Redis (caching)
- Elasticsearch (code search), libgit2 (Git operations)

## Lessons Learned

1. **Lazy computation beats eager computation** — Computing diffs on-demand with caching is more efficient than pre-computing
2. **Three-replica synchronous writes ensure durability** — Git repository loss is catastrophic; replication is non-negotiable
3. **Code review is sociotechnical** — CODEOWNERS and branch protection rules encode organizational policies into workflow
4. **Merge queues solve semantic conflicts** — Testing PRs in isolation is insufficient; merge queues test combined results
5. **Incremental migration works** — Moving from monolith to microservices incrementally, optimizing hot paths first

## Further Reading

- [GitHub Engineering Blog](https://github.blog/category/engineering/)
- [How We Build GitHub](https://github.blog/2023-02-15-how-we-build-github/)
